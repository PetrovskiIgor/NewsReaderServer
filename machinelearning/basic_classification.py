__author__ = 'igorpetrovski'



class BasicClassificator:


    def __init__(self, categories):
        self.ind_to_cat = []
        self.cat_to_ind = {}

        ind = 0

        for cat in categories:

            if not cat  in self.cat_to_ind:

                self.cat_to_ind[cat] = ind
                self.ind_to_cat.append(cat)
                ind += 1


    def transform_to_vector_space(self, inputs, outputs):

        y = []

        X = self.vectorizer.fit_transform(inputs)

        for output in outputs:
            y.append(self.cat_to_ind[output])


        return X, y