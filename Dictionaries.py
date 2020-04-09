
class Dictionary():

    def __init__(self):
        
        self.dict_object = {}


    def choose_dict(self, dict_type):

        if dict_type == "action":
            self.create_action_dict()
        elif dict_type == "number":
            self.create_number_dict()
        elif dict_type == "number_rank":
            self.create_number_rank_dict()
        elif dict_type == "rank_number":
            self.create_rank_number_dict()
        else:
            self.create_suit_dict()

    
    # creates a dictionary of form '2c': 0
    def create_action_dict(self):

        # clubs
        self.dict_object['2c'] = 0
        self.dict_object['3c'] = 1
        self.dict_object['4c'] = 2
        self.dict_object['5c'] = 3
        self.dict_object['6c'] = 4
        self.dict_object['7c'] = 5
        self.dict_object['8c'] = 6
        self.dict_object['9c'] = 7
        self.dict_object['Tc'] = 8
        self.dict_object['Jc'] = 9
        self.dict_object['Qc'] = 10
        self.dict_object['Kc'] = 11
        self.dict_object['Ac'] = 12
        
        # diamonds
        self.dict_object['2d'] = 13
        self.dict_object['3d'] = 14
        self.dict_object['4d'] = 15
        self.dict_object['5d'] = 16
        self.dict_object['6d'] = 17
        self.dict_object['7d'] = 18
        self.dict_object['8d'] = 19
        self.dict_object['9d'] = 20
        self.dict_object['Td'] = 21
        self.dict_object['Jd'] = 22
        self.dict_object['Qd'] = 23
        self.dict_object['Kd'] = 24
        self.dict_object['Ad'] = 25

        # hearts
        self.dict_object['2h'] = 26
        self.dict_object['3h'] = 27
        self.dict_object['4h'] = 28
        self.dict_object['5h'] = 29
        self.dict_object['6h'] = 30
        self.dict_object['7h'] = 31
        self.dict_object['8h'] = 32
        self.dict_object['9h'] = 33
        self.dict_object['Th'] = 34
        self.dict_object['Jh'] = 35
        self.dict_object['Qh'] = 36
        self.dict_object['Kh'] = 37
        self.dict_object['Ah'] = 38

        # spades
        self.dict_object['2s'] = 39
        self.dict_object['3s'] = 40
        self.dict_object['4s'] = 41
        self.dict_object['5s'] = 42
        self.dict_object['6s'] = 43
        self.dict_object['7s'] = 44
        self.dict_object['8s'] = 45
        self.dict_object['9s'] = 46
        self.dict_object['Ts'] = 47
        self.dict_object['Js'] = 48
        self.dict_object['Qs'] = 49
        self.dict_object['Ks'] = 50
        self.dict_object['As'] = 51

    
    def create_number_dict(self):

        # clubs
        self.dict_object[0] = '2c'
        self.dict_object[1] = '3c'
        self.dict_object[2] = '4c'
        self.dict_object[3] = '5c'
        self.dict_object[4] = '6c'
        self.dict_object[5] = '7c'
        self.dict_object[6] = '8c'
        self.dict_object[7] = '9c'
        self.dict_object[8] = 'Tc'
        self.dict_object[9] = 'Jc'
        self.dict_object[10] = 'Qc'
        self.dict_object[11] = 'Kc'
        self.dict_object[12] = 'Ac'
        
        # diamonds
        self.dict_object[13] = '2d'
        self.dict_object[14] = '3d'
        self.dict_object[15] = '4d'
        self.dict_object[16] = '5d'
        self.dict_object[17] = '6d'
        self.dict_object[18] = '7d'
        self.dict_object[19] = '8d'
        self.dict_object[20] = '9d'
        self.dict_object[21] = 'Td'
        self.dict_object[22] = 'Jd'
        self.dict_object[23] = 'Qd'
        self.dict_object[24] = 'Kd'
        self.dict_object[25] = 'Ad'

        # hearts
        self.dict_object[26] = '2h'
        self.dict_object[27] = '3h'
        self.dict_object[28] = '4h'
        self.dict_object[29] = '5h'
        self.dict_object[30] = '6h'
        self.dict_object[31] = '7h'
        self.dict_object[32] = '8h'
        self.dict_object[33] = '9h'
        self.dict_object[34] = 'Th'
        self.dict_object[35] = 'Jh'
        self.dict_object[36] = 'Qh'
        self.dict_object[37] = 'Kh'
        self.dict_object[38] = 'Ah'

        # spades
        self.dict_object[39] = '2s'
        self.dict_object[40] = '3s'
        self.dict_object[41] = '4s'
        self.dict_object[42] = '5s'
        self.dict_object[43] = '6s'
        self.dict_object[44] = '7s'
        self.dict_object[45] = '8s'
        self.dict_object[46] = '9s'
        self.dict_object[47] = 'Ts'
        self.dict_object[48] = 'Js'
        self.dict_object[49] = 'Qs'
        self.dict_object[50] = 'Ks'
        self.dict_object[51] = 'As'


    def create_number_rank_dict(self):

        self.dict_object[10] = 'T'
        self.dict_object[11] = 'J'
        self.dict_object[12] = 'Q'
        self.dict_object[13] = 'K'
        self.dict_object[14] = 'A'


    def create_rank_number_dict(self):

        self.dict_object['T'] = 10
        self.dict_object['J'] = 11
        self.dict_object['Q'] = 12
        self.dict_object['K'] = 13
        self.dict_object['A'] = 14


    def create_suit_dict(self):

        self.dict_object['c'] = 0
        self.dict_object['d'] = 1
        self.dict_object['s'] = 2
        self.dict_object['h'] = 3
