import re

class Analizer():
    cp = [
        {'txt':'tidak ramah', 'nilai':-1},
        {'txt':'tidak suka', 'nilai':-1},
        {'txt':'rasanya hambar', 'nilai':-1},
        {'txt':'harganya mahal', 'nilai':-1},
        {'txt':'harga mahal', 'nilai':-1},
        {'txt':'tempatnya kotor', 'nilai':-1},
        {'txt':'tempat kotor', 'nilai':-1},
        {'txt':'tempatnya tidak bersih', 'nilai':-1},
        {'txt':'tempat tidak bersih', 'nilai':-1},
        {'txt':'rasanya enak', 'nilai':1},
        {'txt':'rasa enak', 'nilai':1},
        {'txt':'harga murah', 'nilai':1},
        {'txt':'harganya murah', 'nilai':1},
    ]

    def proses(self, data):
        text = data
        text = re.sub(r'\,', '.', text)

        text = text.split('.')

        nilai = 0
        for nn in text:
            mm = nn.strip()
            for oo in self.cp:
                if oo['txt'] in mm:
                    nilai = nilai + oo['nilai']
        return nilai
