Tekst projektnog zadatka:

Implementirati na programskom jeziku Python:

1. Algoritam za indeksirano pretraživanje stringova u zadatom tekstu koristeći Burrows-Wheeler transformaciju i FM index. Inicijalna verzija algoritma treba da bude realizovana na tradicionalan način opisan na predavanju, bez optimizacije memorije i vremena izvršavanja (10 poena).
2. Algoritam za globalno poravnavanje stringova (global alignment - Needleman-Wunsch) koji koristi skoring tabelu (scoring matrix) gde je vrednost poklapanja (match) 1, mutacije (mismatch) -3 i insercije ili delecije (gap) -7. Izlaz funkcije je torka (tuple) koju čine optimalna ocena poravnanja (optimal global alignment score) i edit transkript (npr. “MMMMRMMI”) (5 poena).
3. Program prima kao ulaz referencu (FASTA fajl) i kolekciju ridova (FASTQ fajl) i za svaki od ridova vraća listu torki (pozicija gde se rid mapira na referencu, ocena optimalnog poravnanja na toj poziciji i edit transkript) - liste treba sortirati po oceni od najveće ka najmanjoj. Koristiti “Seed & Extend” metod gde se seed uzima sa početka rida (dužina seed-a je ulazni parametar), za lociranje pozicije seed-a u referenci koristiti algoritam iz tačke (1). Zatim, preostali deo rida treba poravnati na odgovarajući deo reference iza lociranog seed-a koristeći algoritam iz tačke (2). Deo reference na koji se preostali deo rida poravnava treba biti duži od preostalog dela rida za 0 - 10 nukleotide (ulazni parametar “margin”). (5 poena).
4. Dati dijagrame poređenja vremena izvršavanja i prosečne ocene optimalnog poravnanja ridova (koristiti samo jednu, najvišu ocenu za svaki rid) za dužinu seed-a 10, 15 i 20 nukleotida i “margin” parametar 0 i 10 (testirati svih 6 kombinacija). Za testiranje koristiti dati referentni genom i kolekciju ridova. Prikazati rezultate tabelarno i grafički (5 poena).

 5. Pripremiti prezentaciju (Google slides ili power point) implementiranog rešenja, kao i samih rezultata (5 poena).
6. Pripremiti video prezentaciju projekta (3 - 5 minuta trajanja) koja će biti dostupna na YouTube ili drugom on-line video servisu (10 poena).

Pokretanje programa:

Pokrenuti program.py i proslediti neophodne parametre:

	-a: putanja do FASTA fajla
	-q: putanja do FASTQ fajla
	-s: niz seed parametara odvojenih space karakterom
	-m: niz margin parametara odvojenih space karakterom

Link ka Google Slides prezentaciji:
https://docs.google.com/presentation/d/1TnYzKvrOvqpvP2B2-zE6nnCortknE4qvaaevPZeffvU/edit#slide=id.g4dfce81f19_0_45

Link ka video prezentaciji:
https://www.youtube.com/watch?v=aM2A1avYik0&feature=youtu.be
