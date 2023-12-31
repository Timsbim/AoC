def run_monad_reduced(model_number):
    w = x = y = z = 0
    
    w_0 = int(model_number[0])
    z_0 = (w_0 + 10)
    
    w_1 = int(model_number[1])
    z_1 = z_0 * 26 + (w_1 + 16)
    
    w_2 = int(model_number[2])
    z_2 = z_1 * 26 + (w_2 + 0)
    
    w_3 = int(model_number[3])
    z_3 = z_2 * 26 + (w_3 + 13)
    
    w_4 = int(model_number[4])
    x = z_3 % 26 - 14  # x == w_3 + 13
    x = 0 if x == w_4 else 1  #  w_3 + 13 == w_4 - 14 -> w_4 = w_3 - 1
    z_3 = z_2 
    z_4 = z_3 * (25 * x + 1) + x * (w_4 + 7)  # z_4 == z_2

    w_5 = int(model_number[5])
    x = z_4 % 26 - 4  # x == w_2 - 4
    x = 0 if x == w_5 else 1  # w_5 == w_2 - 4
    z_4 //= 26  # z_4 == z_1
    z_5 = z_4 * (25 * x + 1) + x * (w_5 + 11)  # z_5 == z_1
    
    w_6 = int(model_number[6])
    z_6 = z_5 * 26 + (w_6 + 11)  # z_6 == z_1 * 26 + (w_6 + 11)
    
    w_7 = int(model_number[7])
    x = z_6 % 26 - 3  # x == w_6 + 11 - 2 == w_6 + 8
    x = 0 if x == w_7 else 1  # w_7 == w_6 + 8 -> w_6 == 1 & w_7 == 9
    z_6 = z_5  # z_6 == z_1
    z_7 = z_6 * (25 * x + 1) + x * (w_7 + 10)  # z_7 == z_1
    
    w_8 = int(model_number[8])
    z_8 = z_7 * 26 + (w_8 + 16)  # z_8 == z_1 * 26 + (w_8 + 16)
    
    w_9 = int(model_number[9])
    x = z_8 % 26 - 12  # x == w_8 + 16 - 12 == w_8 + 4
    x = 0 if x == w_9 else 1  # w_9 == w_8 + 4
    z_8 = z_7  # z_8 == z_1
    z_9 = z_8 * (25 * x + 1) + x * (w_9 + 8)  # z_9 == z_1
    
    w_10 = int(model_number[10])
    z_10 = z_9 * 26 + (w_10 + 15)  # z_10 == z_1 * 26 + (w_10 + 15)
    
    w_11 = int(model_number[11])
    x = z_10 % 26 - 12  # x == w_10 + 15 - 12 == w_10 + 3
    x = 0 if x == w_11 else 1  # w_11 == w_10 + 3
    z_10 = z_9  # z_10 == z_1
    z_11 = z_10 * (25 * x + 1) + x * (w_11 + 2)  # z_11 == z_1
    
    w_12 = int(model_number[12])
    x = z_11 % 26 - 15  # x = w_1 + 16 - 15 == w_1 + 1
    x = 0 if x == w_12 else 1  # w_12 == w_1 + 1
    z_11 //= 26  # z_11 = z_0
    z_12 = z_11 * (25 * x + 1) + x * (w_12 + 5)  # z_12 == z_0 
    
    w_13 = int(model_number[13])
    x = z_12 % 26 - 12  # x == w_0 + 10 - 12 = w_0 - 2
    x = 0 if x == w_13 else 1  # w_13 == w_0 - 2
    z_12 //= 26  # z_12 == 0
    z_13 = z_12 * (25 * x + 1) + x * (w_13 + 10)
    
    return z_13

"""
    w_4 = w_3 - 1
    w_5 == w_2 - 4
    w_6 == 1 & w_7 == 9
    w_9 == w_8 + 4
    w_11 == w_10 + 3
    w_12 == w_1 + 1
    w_13 == w_0 - 2

    9899 8519 5969 97
"""