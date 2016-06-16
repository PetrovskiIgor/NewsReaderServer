from sklearn import datasets, svm, metrics
digits = datasets.load_digits()
 
sliki = list(zip(digits.images, digits.target))
 
asd = len(digits.images)
data = digits.images.reshape((asd, -1))
 
classifier = svm.SVC(gamma=0.001)
 
classifier.fit(data[:asd / 2], digits.target[:asd / 2])
 
izlez = digits.target[asd / 2:]
predict = classifier.predict(data[asd / 2:])
 
print classifier.score(data[asd/2:], digits.target[asd/2:])