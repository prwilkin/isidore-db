import unittest
from backend.app.encrypt import generate_key, encrypt_data, decrypt_data


class MyTestCase(unittest.TestCase):
    def test_function(self):
        password = "string"
        txt = "Hello world"
        print(password, " ", txt)
        encrypted_data, iv, salt = encrypt_data(txt, password)  # Encrypt with dynamic salt
        print(f'{encrypted_data}, {iv}, {salt}')
        decrypted_data = decrypt_data(encrypted_data, password, iv, salt)  # Decrypt using stored salt
        print(decrypted_data)
        self.assertEqual(txt, decrypted_data)


if __name__ == '__main__':
    unittest.main()
