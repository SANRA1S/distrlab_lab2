class MyBigInt:
    def __init__(self):
        self.data = []

    def setHex(self, hex_str):
        self.data = []
        for i in range(0, len(hex_str), 8): # Форматуєм строку у масив по 8 біт
            chunk = hex_str[i:i + 8]
            self.data.append(int(chunk, 16))
    def getHex(self):
        return self.__str__()

    def XOR(self, other):
        result = MyBigInt()
        for i in range(max(len(self.data), len(other.data))):# Перевірка довжиа А = В
            num1 = self.data[i] if i < len(self.data) else 0
            num2 = other.data[i] if i < len(other.data) else 0
            result.data.append(self.data[i] ^ other.data[i])
        return result

    def OR(self,  other):
        result = MyBigInt()
        for i in range(max(len(self.data), len(other.data))):
            num1 = self.data[i] if i < len(self.data) else 0
            num2 = other.data[i] if i < len(other.data) else 0
            result.data.append(num1 | num2)
        return result

    def AND(self, other):
        result = MyBigInt()
        for i in range(max(len(self.data), len(other.data))):
            num1 = self.data[i] if i < len(self.data) else 0
            num2 = other.data[i] if i < len(other.data) else 0
            result.data.append(num1 & num2)
        return result

    def INV(self):
        inverted = []
        for i in self.data:
            inverted_num = ~i & 0xFFFFFFFF
            inverted.append(inverted_num)
        result = MyBigInt()
        result.data = inverted
        return result

    def shiftR(self, n):
        blocks = n // 32
        block_shift = n % 32
        result = MyBigInt()
        result.data = self.data.copy()
        result.data = result.data[blocks:]
        if block_shift > 0 and len(result.data) > 0:
            last_block = result.data[-1]#Останній біт
            preserved_bits = 32 - block_shift#кількістьпотрібних бітів
            result.data[-1] = last_block >> block_shift
            result.data[-1] &= (1 << preserved_bits) - 1
        return result

    def shiftL(self, n):
        blocks = n // 32
        block_shift = n % 32
        result = MyBigInt()
        result.data = self.data.copy()
        for i in range(len(self.data)):
            result.data[i] <<= block_shift
            if i < len(result.data) - 1:
                result.data[i + 1] |= (result.data[i] >> 32)
        if blocks > 0:
            result.data.extend([0] * blocks)
        return result

    def add(self, other):
        max_len = max(len(self.data), len(other.data))

        self_ = [0] * (max_len - len(self.data)) + self.data
        other = [0] * (max_len - len(other.data)) + other.data
        result = []
        carry = 0
        for i in range(max_len - 1, -1, -1):
            digit_sum = self_[i] + other[i] + carry
            result.append(digit_sum & 0xffffffff)  # Залишаємо тільки 32 молодших біта
            carry = digit_sum >> 32
        if carry != 0:
            result.append(carry)
        result.reverse()
        res = MyBigInt()
        res.data = result
        return res

    def sub(self, other):
        result = MyBigInt()
        result.data = self.data[:]
        if len(other.data) >= len(self.data):
            for i in range(len(self.data)):
                result.data[i] -= other.data[i]
                if result.data[i] < 0:
                    j = i + 1
                    while j < len(result.data) and result.data[j] == 0:
                        j += 1
                    if j == len(result.data):
                        print("Negative result")
                    result.data[j] -= 1
                    for k in range(i + 1, j):
                        result.data[k] = 0xFFFFFFFF
                    result.data[i] += 0x100000000
        else:
            print("Negative result")

        # Удаляем ведущие нули
        while len(result.data) > 1 and result.data[-1] == 0:
            result.data.pop()

        return result

    def mod(self, modulus):
        mod_len = len(hex(modulus)[2:])
        num_len = len(self.data)
        if num_len < mod_len:
            return self
        remainder = MyBigInt()
        temp = MyBigInt()
        for i in range(num_len):
            temp.data.append(self.data[i])
            if len(temp.data) == mod_len:
                quotient = MyBigInt()
                div = 0
                for j in range(mod_len - 1, -1, -1):
                    div = (div << 32) | temp.data[j]
                    quotient.data.insert(0, div // modulus)
                    div %= modulus
                remainder.data.insert(0, div)
                temp.data = []
        if len(temp.data) > 0:
            remainder.data = temp.data
        return remainder

    def __str__(self):
        hex_str = ""
        for num in self.data:
            hex_str += format(num, "08x")
        return hex_str


numberA = MyBigInt()
numberB = MyBigInt()
numberA.setHex("36f028580bb02cc8272a9a020f4200e346e276ae664e45ee80745574e2f5ab80")
numberB.setHex("70983d692f648185febe6d6fa607630ae68649f7e6fc45b94680096c06e4fadb")
print("Data type : " + str(type(numberA)))
print("A : " + numberA.getHex())
print("A + B : " + str(numberA.add(numberB)))
print("A - B : " + str(numberA.sub(numberB)))
print("A % 10 : " + str(numberA.mod(10)))
print("A XOR B : " + str(numberA.XOR(numberB)))  # выведет "e035c6cfa42609b998b883bc1699df885cef74e2b2cc372eb8fa7e7"
print("INV A : " + str(numberA.INV()))
print("A OR B : " + str(numberA.OR(numberB)))
print("A AND B : " + str(numberA.AND(numberB)))
print("A shift 4 bit right : " + str(numberA.shiftR(4)))
print("A shift 4 bit left : " + str(numberA.shiftL(4)))
