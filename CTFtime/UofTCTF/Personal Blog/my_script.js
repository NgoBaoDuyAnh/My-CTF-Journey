const crypto = require('crypto');
const POW_VERSION = 's';
exports.POW_VERSION = POW_VERSION;
const POW_MOD = (1n << 1279n) - 1n;
const POW_ONE = 1n;
const mySol = 1337n;
const difficulty = 5000;

function bigIntToBuffer(bn) {
  let hex = bn.toString(16);
  if (hex.length % 2) { hex = '0' + hex; }
  let buf = Buffer.from(hex, 'hex');
  return buf
}

function powGenerateChallenge(bytes) {
  const Bytes = Buffer.alloc(4);
  Bytes.writeUInt32BE(difficulty);
  return `${POW_VERSION}.${Bytes.toString('base64')}.${bytes.toString('base64')}`;
}

function powGenerateSolution() {
    let current = mySol;
    for (let i = 0; i< difficulty; i +=1) {
        current = (current ^ POW_ONE);
        current = (current * current) % POW_MOD;
    }

    const bytes = bigIntToBuffer(current);
    console.log(powGenerateChallenge(bytes,difficulty))

    const encoded_sol = bigIntToBuffer(mySol);
    console.log(`${POW_VERSION}.${encoded_sol.toString('base64')}`)
    return current;

}

powGenerateSolution();
