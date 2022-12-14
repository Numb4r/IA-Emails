import unicodedata
import re
import mailparser


class email:
    def __init__(self, typeEmail, body) -> None:
        self.typeEmail
        self.body = body


"""
listBody = lista de palavras ja tratadas do corpo do email
listWords = lista de palavras que tem no email, nao repetidas
mapCountWords = dict com a quantidade de ocorrencias de cada palavra no email
arrayMappingWords = array de posicao para a formacao de tabela com a frequencia de palavras
"""


class bodyEmail:
    def __init__(self, listBody, typeEmail=None):
        self.listBody = listBody
        self.typeEmail = typeEmail
        self.listWords = set()
        self.mapCountWords = {}
        self.arrayMappingWorlds = []

        self._filterWords()
        self._listUniqueWords()
        self._countWords()

    def _countWords(self):
        if len(self.listWords) == 0:
            print('Unable to count Words in file ${folder}')
        else:
            for i in self.listWords:
                self.mapCountWordsWords[i] = self.listBody.count(i)

    def _filterWords(self):
        self.listBody = unicodedata.normalize("NFKD", self.listBody)
        self.listBody = re.sub(r"\n", r" ", self.listBody)

        self.listBody = re.sub(
            r"(?P<letter>[^\d\s])(?P<number>\d)", "\g<1> \g<2>", self.listBody)
        self.listBody = re.sub(
            r"(?P<number>\d)(?P<letter>[^\d\s])", "\g<1> \g<2>", self.listBody)
        self.listBody = re.sub(
            r"(?P<signal>[^A-Za-z0-9\s])(?P<letter>[a-z0-9])", "\g<1> \g<2>", self.listBody)  # separar l,
        self.listBody = re.sub(
            r"(?P<letter>[a-z0-9])(?P<signal>[^A-Za-z0-9\s])", "\g<1> \g<2>", self.listBody)  # separar ,l

        self.listBody = re.sub(r"\b\d{1,5}\b", r" \!_NUMBER ", self.listBody)
        # Substituir grandes numeros
        self.listBody = re.sub(r"\b\d{6,}\b", r" \!_BIGNUMBER ", self.listBody)
        # TODO: Capturar apostrofos
        # Eliminar word{l < 3}
        self.listBody = re.sub(r"\b\w{1,2}\b", r"", self.listBody)
        # caracteres especiais
        self.listBody = re.sub(r"(?<!\!)[^\w\s](?!_)", r"", self.listBody)
        self.listBody = list(self.listBody.split(" "))
        while ("" in self.listBody):
            self.listBody.remove("")
        # print(self.listBody)

    def __str__(self) -> str:
        return " ".join(self.listBody)

    def _listUniqueWords(self):
        self.listWords = set(self.listBody)

    def getListWords(self):
        return self.listWords

    def _countWords(self):
        if len(self.listWords) == 0:
            return
            # raise 'Unable to count Words'
        for i in self.listWords:
            self.mapCountWords[i] = self.listBody.count(i)
        # self.mapCountWords

    def get_mapCountWords(self):
        return self.mapCountWords


class header:
    def __init__(self, listHeader):
        self.listHeader = listHeader

    def __str__(self) -> str:
        return "".join(self.listHeader)


def getBody(t, typeEmail=None):
    mail = mailparser.parse_from_string(t)

    # headerStrList = []
    # body = False
    # bodyStrList = []

    # for i in t.splitlines():
    #     if not body:  # header capture
    #         headerStrList.append(i)
    #         if re.findall(r"Content\-Transfer\-Encoding:.*", i):
    #             h = header(headerStrList)
    #             headerStrList = []
    #             body = True
    #     else:
    #         bodyStrList.append(i)
    #         if i == t.splitlines()[-1]:
    #             b = bodyEmail(bodyStrList)

    return bodyEmail(mail.body, typeEmail)
