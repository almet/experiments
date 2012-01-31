#include <iostream>

#include "cryptopp/rsa.h"
#include "cryptopp/osrng.h"
#include "cryptopp/integer.h"
#include "cryptopp/sha.h"
#include "cryptopp/hex.h"
#include "cryptopp/filters.h"

/**
 * Simple use of Crypto++ to sign a text with RSA
 **/

using namespace std;
using namespace CryptoPP;

int main(int argc, const char *argv[])
{
    
    // monty pythons!
    string text = "Are you suggesting coconuts migrate?";
    AutoSeededRandomPool rng;

    InvertibleRSAFunction keys;
    keys.GenerateRandomWithKeySize(rng, 384);

    RSASS<PKCS1v15, SHA>::Signer signer(keys);

    byte* signature = new byte[signer.MaxSignatureLength()];
    if(NULL == signature) { return -1; }

    // Sign...
    size_t length = signer.SignMessage(rng, (const byte*) text.c_str(),
                                       text.length(), signature);

    RSASS<PKCS1v15, SHA>::Verifier verifier(signer);

    bool result = verifier.VerifyMessage((const byte*)text.c_str(),
                                         text.length(), signature, length);

    return 0;
}
