
class Dictionary(object):

    def __init__(self, is_card):
        
        self.is_card = is_card
        self.card_dict = {}


    def choose_dict(self, is_card):

        if is_card:
            self.create_action_dict()
        else:
            self.create_number_dict()

    
    # creates a dictionary of form '2c': 0
    def create_action_dict(self):

        # clubs
        self.card_dict['2c'] = 0
        self.card_dict['3c'] = 1
        self.card_dict['4c'] = 2
        self.card_dict['5c'] = 3
        self.card_dict['6c'] = 4
        self.card_dict['7c'] = 5
        self.card_dict['8c'] = 6
        self.card_dict['9c'] = 7
        self.card_dict['Tc'] = 8
        self.card_dict['Jc'] = 9
        self.card_dict['Qc'] = 10
        self.card_dict['Kc'] = 11
        self.card_dict['Ac'] = 12
        
        # diamonds
        self.card_dict['2d'] = 13
        self.card_dict['3d'] = 14
        self.card_dict['4d'] = 15
        self.card_dict['5d'] = 16
        self.card_dict['6d'] = 17
        self.card_dict['7d'] = 18
        self.card_dict['8d'] = 19
        self.card_dict['9d'] = 20
        self.card_dict['Td'] = 21
        self.card_dict['Jd'] = 22
        self.card_dict['Qd'] = 23
        self.card_dict['Kd'] = 24
        self.card_dict['Ad'] = 25

        # hearts
        self.card_dict['2h'] = 26
        self.card_dict['3h'] = 27
        self.card_dict['4h'] = 28
        self.card_dict['5h'] = 29
        self.card_dict['6h'] = 30
        self.card_dict['7h'] = 31
        self.card_dict['8h'] = 32
        self.card_dict['9h'] = 33
        self.card_dict['Th'] = 34
        self.card_dict['Jh'] = 35
        self.card_dict['Qh'] = 36
        self.card_dict['Kh'] = 37
        self.card_dict['Ah'] = 38

        # spades
        self.card_dict['2s'] = 39
        self.card_dict['3s'] = 40
        self.card_dict['4s'] = 41
        self.card_dict['5s'] = 42
        self.card_dict['6s'] = 43
        self.card_dict['7s'] = 44
        self.card_dict['8s'] = 45
        self.card_dict['9s'] = 46
        self.card_dict['Ts'] = 47
        self.card_dict['Js'] = 48
        self.card_dict['Qs'] = 49
        self.card_dict['Ks'] = 50
        self.card_dict['As'] = 51

        return self.card_dict

    
    def create_number_dict(self):

        # clubs
        self.card_dict[0] = '2c'
        self.card_dict[1] = '3c'
        self.card_dict[2] = '4c'
        self.card_dict[3] = '5c'
        self.card_dict[4] = '6c'
        self.card_dict[5] = '7c'
        self.card_dict[6] = '8c'
        self.card_dict[7] = '9c'
        self.card_dict[8] = 'Tc'
        self.card_dict[9] = 'Jc'
        self.card_dict[10] = 'Qc'
        self.card_dict[11] = 'Kc'
        self.card_dict[12] = 'Ac'
        
        # diamonds
        self.card_dict[13] = '2d'
        self.card_dict[14] = '3d'
        self.card_dict[15] = '4d'
        self.card_dict[16] = '5d'
        self.card_dict[17] = '6d'
        self.card_dict[18] = '7d'
        self.card_dict[19] = '8d'
        self.card_dict[20] = '9d'
        self.card_dict[21] = 'Td'
        self.card_dict[22] = 'Jd'
        self.card_dict[23] = 'Qd'
        self.card_dict[24] = 'Kd'
        self.card_dict[25] = 'Ad'

        # hearts
        self.card_dict[26] = '2h'
        self.card_dict[27] = '3h'
        self.card_dict[28] = '4h'
        self.card_dict[29] = '5h'
        self.card_dict[30] = '6h'
        self.card_dict[31] = '7h'
        self.card_dict[32] = '8h'
        self.card_dict[33] = '9h'
        self.card_dict[34] = 'Th'
        self.card_dict[35] = 'Jh'
        self.card_dict[36] = 'Qh'
        self.card_dict[37] = 'Kh'
        self.card_dict[38] = 'Ah'

        # spades
        self.card_dict[39] = '2s'
        self.card_dict[40] = '3s'
        self.card_dict[41] = '4s'
        self.card_dict[42] = '5s'
        self.card_dict[43] = '6s'
        self.card_dict[44] = '7s'
        self.card_dict[45] = '8s'
        self.card_dict[46] = '9s'
        self.card_dict[47] = 'Ts'
        self.card_dict[48] = 'Js'
        self.card_dict[49] = 'Qs'
        self.card_dict[50] = 'Ks'
        self.card_dict[51] = 'As'

        return self.card_dict
