import simplerlangParser
from simplerlangListener import simplerlangListener


class simplerlangListenerExtended(simplerlangListener):

    def exitLet(self, ctx:simplerlangParser.LetContext):
