EVALUATE_MATRIX = [[500,-25,10,5,5,10,-25,500],
[-25,-45,1,1,1,1,-45,-25],
[10,1,3,2,2,3,1,10],
[5,1,2,1,1,2,1,5],
[5,1,2,1,1,2,1,5],
[10,1,3,2,2,3,1,10],
[-25,-45,1,1,1,1,-45,-25],
[500,-25,10,5,5,10,-25,500]]

def evaluate(chess): 
    assert len(chess) == 64
    ans = 0 
    for i in range(8): 
        for j in range(8): 
            ans += chess[i * 8 + j] * EVALUATE_MATRIX[i][j] 
    return -ans 


EVALUATE_MATRIX2 = [[200,-25,10,5,5,10,-25,200],
[-25,-45,1,1,1,1,-45,-25],
[10,1,3,2,2,3,1,10],
[5,1,2,1,1,2,1,5],
[5,1,2,1,1,2,1,5],
[10,1,3,2,2,3,1,10],
[-25,-45,1,1,1,1,-45,-25],
[200,-25,10,5,5,10,-25,200]]

def evaluate2(chess): 
    assert len(chess) == 64
    ans = 0 
    for i in range(8): 
        for j in range(8): 
            ans += chess[i * 8 + j] * EVALUATE_MATRIX2[i][j] 
    return -ans 

EVALUATE_MATRIX3 = [[200,-40,10,5,5,10,-40,200],
[-40,30,1,1,1,1,30,-40],
[10,1,3,2,2,3,1,10],
[5,1,2,1,1,2,1,5],
[5,1,2,1,1,2,1,5],
[10,1,3,2,2,3,1,10],
[-40,30,1,1,1,1,30,-40],
[200,-40,10,5,5,10,-40,200]]

def evaluate3(chess): 
    assert len(chess) == 64
    ans = 0 
    for i in range(8): 
        for j in range(8): 
            ans += chess[i * 8 + j] * EVALUATE_MATRIX3[i][j] 
    return -ans 

EVALUATE_MATRIX4 = [[20, -3, 11, 8, 8, 11, -3, 20],
[-3, -7, -4, 1, 1, -4, -7, -3],
[11, -4, 2, 2, 2, 2, -4, 11],
[8, 1, 2, -3, -3, 2, 1, 8],
[8, 1, 2, -3, -3, 2, 1, 8],
[11, -4, 2, 2, 2, 2, -4, 11],
[-3, -7, -4, 1, 1, -4, -7, -3],
[20, -3, 11, 8, 8, 11, -3, 20]] 

def evaluate4(chess): 
    assert len(chess) == 64
    ans = 0 
    for i in range(8): 
        for j in range(8): 
            ans += chess[i * 8 + j] * EVALUATE_MATRIX4[i][j] 
    return -ans 