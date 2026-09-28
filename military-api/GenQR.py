import qrcode

def generate_qr_code(url, filename):
    # Create a QR Code object
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each box in pixels
        border=4,  # Thickness of the border (minimum is 4)
    )

    # Add data to the QR Code
    qr.add_data(url)
    qr.make(fit=True)  # Fit the QR code to the data

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a file
    img.save(filename)
    print(f"QR Code generated and saved as {filename}")

# Example usage
url_to_encode = "https://cos.nrru.ac.th/BookingAPP/"  # Replace with your URL
output_filename = "BookingAPP.png"  # Name of the output file
generate_qr_code(url_to_encode, output_filename)
