from essential_generators import DocumentGenerator

gen = DocumentGenerator()

for i in range(3000):
	print(gen.sentence().replace('\n', ' '))
