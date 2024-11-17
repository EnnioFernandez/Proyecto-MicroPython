from time import sleep_ms

class LCD:
    def __init__(self, i2c, addr=0x27):
        self.i2c = i2c
        self.addr = addr
        self.backlight = 0x08  # Backlight ON by default
        self.init_lcd()

    def send(self, data, mode=0):
        high_nibble = (data & 0xF0) | mode | self.backlight | 0x04  # Enable High
        low_nibble = ((data << 4) & 0xF0) | mode | self.backlight | 0x04  # Enable Low
        self.i2c.writeto(self.addr, bytes([high_nibble]))
        sleep_ms(1)
        self.i2c.writeto(self.addr, bytes([high_nibble & ~0x04]))  # Disable
        self.i2c.writeto(self.addr, bytes([low_nibble]))
        sleep_ms(1)
        self.i2c.writeto(self.addr, bytes([low_nibble & ~0x04]))  # Disable

    def init_lcd(self):
        sleep_ms(50)
        self.send(0x30)
        sleep_ms(5)
        self.send(0x30)
        sleep_ms(1)
        self.send(0x30)
        sleep_ms(1)
        self.send(0x20)  # 4-bit mode
        self.command(0x28)  # 4-bit, 2 lines, 5x8 dots
        self.command(0x0C)  # Display ON, Cursor OFF
        self.command(0x06)  # Increment cursor
        self.command(0x01)  # Clear display

    def command(self, cmd):
        self.send(cmd, 0x00)

    def write_char(self, char):
        self.send(ord(char), 0x01)

    def write(self, text):
        for char in text:
            self.write_char(char)

    def clear(self):
        self.command(0x01)
        sleep_ms(2)

    def move_to(self, line, col):
        address = col + (0x80 if line == 0 else 0xC0)
        self.command(address)

    def toggle_backlight(self, state):
        self.backlight = 0x08 if state else 0x00
        self.command(0)  # Send a dummy command to update the backlight