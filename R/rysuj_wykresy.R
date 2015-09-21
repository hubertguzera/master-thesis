setwd("C:/Users/Hubert/Desktop/master-thesis/master-thesis/")
getwd()
ludnosc <- read.csv("rezultaty/ludnosc.csv")
png("tekst/pictures/ludnosc.png")
par(mfrow = c(2,2))
hist(ludnosc$zarobki)
hist(ludnosc$wiek)
hist(ludnosc$wyksztalcenie)
hist(ludnosc$kobieta)
dev.off()

wyksztalcenie <- read.csv("dane/wyksztalcenie.csv")
k_w <- wyksztalcenie[wyksztalcenie$Plec=="Kobieta",]
m_w <- wyksztalcenie[wyksztalcenie$Plec=="Mezczyzna",]
par(mfrow = c(1,1))
png("tekst/pictures/wyksztalcenie.png")
plot(k_w$p, col="red", xaxt = 'n',xlab="Wykszta³cenie", ylab="Prawdopodobienstwo", main = 'Rozk³ad zmiennej wykszta³cenie')
axis(1, at=1:4,k_w$Wyksztalcenie)
lines(k_w$p, col="red")
points(m_w$p, col="green")
lines(m_w$p, col="green")
dev.off()

wiek <- read.csv("dane/wiek.csv",header=FALSE)
png("tekst/pictures/wiek.png")
plot(wiek, ylab="Prawdopodobienstwo", xlab="Wiek", main = 'Rozk³ad zmiennej wiek')
dev.off()

