setwd("C:/Users/Hubert/Desktop/master-thesis/master-thesis/")
getwd()
ludnosc <- read.csv("rezultaty/ludnosc.csv")
ludnosc <- ludnosc[,-2]
ludnosc <- ludnosc[,-5]
ludnosc$mezczyzna[ludnosc$mezczyzna==1] <- "Mezczyzna"
ludnosc$mezczyzna[ludnosc$mezczyzna==0] <- "Kobieta"

ludnosc$wyksztalcenie[ludnosc$wyksztalcenie==0] <- "Brak"
ludnosc$wyksztalcenie[ludnosc$wyksztalcenie==1] <- "Podstawowe"
ludnosc$wyksztalcenie[ludnosc$wyksztalcenie==2] <- "Zawodowe"
ludnosc$wyksztalcenie[ludnosc$wyksztalcenie==3] <- "Srednie"
ludnosc$wyksztalcenie[ludnosc$wyksztalcenie==4] <- "Wyzsze"


zainteresowania <- as.data.frame(colSums(ludnosc[5:27]))
colnames(zainteresowania) <- "Iloœæ"
rownames(zainteresowania) <- c("Moda","Gotowanie","Finanse","Kultura","Historia","Koncerty","Motoryzacja","Kosmetyki","Malarstwo","Ogrodnictwo","Gry","Sport","Boks","Fotografia","Kultura alternatywna","Nightlife","Teatr","Ksiazka","Historia polski","Natura","Piwowarstwo","Muzyka klasyczna","Ksiazki")
library(xtable)
print(xtable(zainteresowania))

png("tekst/pictures/ludnosc.png")
par(mfrow = c(2,2))
hist(ludnosc$wiek, main="Histogram zmiennej wiek", xlab = "Wiek")
hist(ludnosc$zarobki, main="Histogram zmiennej zarobki", xlab = "Zarobki" )
plot(as.factor(ludnosc$wyksztalcenie), main="Histogram zmiennej wyksztalcenie")
plot(as.factor(ludnosc$mezczyzna), main="Histogram zmiennej p³eæ")
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


produkty <- read.csv("rezultaty/produkty.csv")
print(xtable(produkty))
dev.off()


prognoza <- read.csv("rezultaty/prognoza.csv")
prognoza <- aggregate(prognoza[3:4], by=list(prognoza$Tura), FUN="sum")
png("tekst/pictures/prog.png")
plot(prognoza$Przewidywane, col="blue", ylim=c(0,as.integer(max(prognoza)*1.25)), xaxt = 'n',xlab="Tura", ylab="Iloœæ produktów", main = 'Prognoza sprzeda¿y i rzeczywista sprzeda¿ produktów')
axis(1, at=1:nrow(prognoza),prognoza$Group.1)
lines(prognoza$Przewidywane, col="blue")
points(prognoza$Sprzedaz, col="green")
lines(prognoza$Sprzedaz, col="green")
dev.off()

