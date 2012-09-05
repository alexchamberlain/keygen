from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
                  render_template, flash
from pprint import pprint
import OpenSSL
import re

# configuration
DATABASE = "database.db"
DEBUG = True
SERVER_CERTIFICATE = "keygen.crt"
SERVER_KEY         = "keygen.key"

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql') as f:
      db.cursor().executescript(f.read())
    db.commit()

def init_server_certificate():
  # Create key pair
  k = OpenSSL.crypto.PKey()
  k.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)

  # Create a Self-Signed Certificate
  c = OpenSSL.crypto.X509()
  s = c.get_subject()
  s.O  = 'keygen test'
  s.CN = 'localhost'
  c.set_serial_number(1000)
  c.gmtime_adj_notBefore(0)
  c.gmtime_adj_notAfter(10*365*24*60*60)
  c.set_issuer(c.get_subject())
  c.set_pubkey(k)
  c.sign(k, 'sha1')

  with open(app.config['SERVER_CERTIFICATE'], "w") as cf:
    cf.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, c))

  with open(app.config['SERVER_KEY'], "w") as cf:
    cf.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, k))

@app.before_request
def before_request():
  g.db = connect_db()
  with open(app.config['SERVER_KEY'], "r") as cf:
    g.key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, cf.read())
  with open(app.config['SERVER_CERTIFICATE'], "r") as cf:
    g.cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cf.read())

@app.teardown_request
def teardown_request(exception):
  g.db.close()

@app.route('/sign-certificate', methods=['POST'])
def sign_certificate():
  pprint('Generating certificate for {}'.format(request.form['username']))
  rawpubkey = re.sub(r'[\r\n]+', '', request.form['public_key'])
  pubkey = OpenSSL.crypto.NetscapeSPKI(rawpubkey).get_pubkey()
  x509   = OpenSSL.crypto.X509()
  x509.set_issuer(g.cert.get_subject())
  x509.set_version(3)
  x509.set_pubkey(pubkey)
  x509.set_serial_number(1000)
  x509.get_subject().CN = request.form['username']
  x509.gmtime_adj_notBefore(0)
  x509.gmtime_adj_notAfter(365*24 * 60 * 60)
  x509.sign(g.key, 'sha1')
  r = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_ASN1, x509)
  return (r, 200, {'Content-Type': 'application/x-x509-user-cert'})

@app.route('/secure', methods=['GET'])
def secure():
  return render_template('secure.html', DN=request.environ['DN'], VERIFIED=request.environ['VERIFIED'])
  

if __name__ == "__main__":
  app.run()
