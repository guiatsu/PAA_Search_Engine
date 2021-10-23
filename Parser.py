class Parser:
    def __init__(self):
        pass

    def get_query_terms(self, query):
        tokens = query.split(" ")

        operators = []
        output = []

        for t in tokens:
            if t == "(":
                operators.append(t)
            elif t == ")":
                while(len(operators) != 0 and operators[-1] != "("):
                    output.append(operators.pop())
                operators.pop()
            elif t in ["AND", "OR", "-"]:
                while(len(operators) != 0 and operators[-1] not in ["(", ")"]):
                    output.append(operators.pop())
                operators.append(t)
            else:
                output.append(t)

        while(len(operators) != 0):
            output.append(operators.pop())

        return output

    def transform_query(self, query):
        # tudo minusculo
        query = query.lower()

        # separa o hifen
        query = query.replace(" -", " - ")

        # operadores AND, OR sao maiusculos
        query = query.replace(" and ", " AND ")
        query = query.replace(" or ", " OR ")

        # adiciona espacos antes e depois de parenteses
        query = query.replace("(", " ( ")
        query = query.replace(")", " ) ")

        # remove espacos duplicados
        query = " ".join(query.split())

        # transforma espacos comuns em "AND"
        new_query = []
        itr = query.split(" ")
        for k in range(len(itr)):
            new_query.append(itr[k])

            if itr[k] not in ["AND", "OR", "-", "(", ")"]:
                if k+1 < len(itr) and itr[k+1] not in ["AND", "OR", "-", "(", ")"]:
                    new_query.append("AND")
            

        return " ".join(new_query)


if __name__ == "__main__":
    #search_sentence(str(input()))
    #print(get_query_terms("((abc or cde) and (bcd and def))"))
    #print(get_query_terms("(abc or (cde and (ghi and def)))"))
    #print(get_query_terms("(((ghi and def) and cde) or abc)"))
    query = "universidade and de or brasilia and darcy -ribeiro"
    #query = "unb -vestibular or (universidade de brasilia)"
    p = Parser()
    query = p.transform_query(query)
    print(query)
    print(p.get_query_terms(query))