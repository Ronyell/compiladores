class Data():

    def return_data(self):
        arq = open('lista.txt', 'r')
        data = arq.read()
        # print(data)
        arq.close()

        return data
