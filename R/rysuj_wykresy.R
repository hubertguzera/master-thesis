setwd("C:/Users/Hubert/Desktop/master-thesis/master-thesis/")
getwd()

#Ludnosc
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


#Rozklady
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

przewidywania <- read.csv("rezultaty/przewidywania.csv")

#Prognozy

prognoza <- read.csv("rezultaty/jeden/prognoza.csv")
prognoza <- aggregate(prognoza[3:4], by=list(prognoza$Tura), FUN="sum")
png("tekst/pictures/prog.png")
plot(prognoza$Przewidywane, col="blue", ylim=c(0,as.integer(max(prognoza)*1.25)), xaxt = 'n',xlab="Tura", ylab="Iloœæ produktów", main = 'Prognoza sprzeda¿y i rzeczywista sprzeda¿ produktów')
axis(1, at=1:nrow(prognoza),prognoza$Group.1)
lines(prognoza$Przewidywane, col="blue")
points(prognoza$Sprzedaz, col="green")
lines(prognoza$Sprzedaz, col="green")
dev.off()

#Wyniki firmy bez optymalizacji

koszty <- read.csv("rezultaty/zero/koszty.csv")
koszty <- aggregate(koszty[6], by=list(koszty$Tura), FUN="sum")
przychody <- read.csv("rezultaty/zero/przychody.csv")
przychody <- aggregate(przychody[5], by=list(przychody$Tura), FUN="sum")
zysk <- read.csv("rezultaty/zero/zysk.csv")
trasy <- read.csv("rezultaty/zero/trasy.csv")
trasy <- aggregate(trasy[c(3,4,5)], by=list(trasy$Tura), FUN="mean")


png("tekst/pictures/brak_algorytmu/wyniki.png")
plot(koszty$Koszt.w.turze, col="red", ylim=c(0,as.integer(max(przychody)*1.25)), xaxt = 'n',xlab="Tura", ylab="PLN", main = 'Wyniki symulacji bez optymalizacji')
axis(1, at=1:nrow(koszty),koszty$Tura)
lines(koszty$Koszt.w.turze, col="red")
points(przychody$Przychod, col="green")
lines(przychody$Przychod, col="green")
points(zysk$Zysk, col="blue")
lines(zysk$Zysk, col="blue")
dev.off()


png("tekst/pictures/brak_algorytmu/trasy.png")
plot(trasy$Koszt, col="red", ylim=c(as.integer(min(trasy)-1.25),as.integer(max(trasy)*1.25)), xaxt = 'n',xlab="Tura", ylab="PLN", main = 'Œrednie wyniki tras')
axis(1, at=1:nrow(trasy),trasy$Tura)
lines(trasy$Koszt, col="red")
points(trasy$Przychod, col="green")
lines(trasy$Przychod, col="green")
points(trasy$Zysk, col="blue")
lines(trasy$Zysk, col="blue")

dev.off()
trasy <- read.csv("rezultaty/jeden/trasy.csv")
png("tekst/pictures/brak_algorytmu/trasy2.png")
ggplot(data = trasy, aes(x = trasy$Tura, y=trasy$Zysk, color = trasy$Symbol)) + ggtitle("Zysk per trasa")+xlab("Zysk") + ylab("Tura")+ geom_line(aes(group=trasy$Symbol)) +geom_point() + theme_bw() + geom_hline(linetype="dashed",aes(yintercept=0))
dev.off()

#Wyniki firmy z optymalizacji
koszty <- read.csv("rezultaty/jeden/koszty.csv")
koszty <- aggregate(koszty[6], by=list(koszty$Tura), FUN="sum")
przychody <- read.csv("rezultaty/jeden/przychody.csv")
przychody <- aggregate(przychody[5], by=list(przychody$Tura), FUN="sum")
zysk <- read.csv("rezultaty/jeden/zysk.csv")
trasy <- read.csv("rezultaty/jeden/trasy.csv")
trasy <- aggregate(trasy[c(3,4,5)], by=list(trasy$Tura), FUN="mean")




png("tekst/pictures/algorytm_brak_skali/wyniki.png")
plot(koszty$Koszt.w.turze, col="red", ylim=c(0,as.integer(max(przychody)*1.25)), xaxt = 'n',xlab="Tura", ylab="PLN", main = 'Wyniki symulacji bez optymalizacji')
axis(1, at=1:nrow(koszty),koszty$Tura)
abline(v = 15, lty = 2)

sredni_zysk = c(1:30)
sredni_zysk[c(1:16)] = mean(zysk$Zysk[c(1:16)]) 
sredni_zysk[c(16:30)] = mean(zysk$Zysk[c(16:25)]) 
sredni_zysk

lines(sredni_zysk,lty = 3,col="purple" )
lines(koszty$Koszt.w.turze, col="red")
points(przychody$Przychod, col="green")
lines(przychody$Przychod, col="green")
points(zysk$Zysk, col="blue")
lines(zysk$Zysk, col="blue")
dev.off()



png("tekst/pictures/algorytm_brak_skali/trasy.png")
plot(trasy$Koszt, col="red", ylim=c(as.integer(min(trasy)-1.25),as.integer(max(trasy)*1.25)), xaxt = 'n',xlab="Tura", ylab="PLN", main = 'Œrednie wyniki tras')
axis(1, at=1:nrow(trasy),trasy$Tura)
lines(trasy$Koszt, col="red")
points(trasy$Przychod, col="green")
lines(trasy$Przychod, col="green")
points(trasy$Zysk, col="blue")
lines(trasy$Zysk, col="blue")

dev.off()
trasy <- read.csv("rezultaty/jeden/trasy.csv")
png("tekst/pictures/algorytm_brak_skali/trasy2.png")
ggplot(data = trasy, aes(x = trasy$Tura, y=trasy$Zysk, color = trasy$Symbol)) + ggtitle("Zysk per trasa")+xlab("Zysk") + ylab("Tura")+ geom_line(aes(group=trasy$Symbol)) +geom_point() + theme_bw() + geom_hline(linetype="dashed",aes(yintercept=0))
dev.off()

#Wyniki firmy z optymalizacji 2
koszty <- read.csv("rezultaty/dwa/koszty.csv")
koszty <- aggregate(koszty[6], by=list(koszty$Tura), FUN="sum")
przychody <- read.csv("rezultaty/dwa/przychody.csv")
przychody <- aggregate(przychody[5], by=list(przychody$Tura), FUN="sum")
zysk <- read.csv("rezultaty/dwa/zysk.csv")
trasy <- read.csv("rezultaty/dwa/trasy.csv")
trasy <- aggregate(trasy[c(3,4,5)], by=list(trasy$Tura), FUN="mean")




png("tekst/pictures/algorytm_skala/wyniki.png")
plot(koszty$Koszt.w.turze, col="red", ylim=c(0,as.integer(max(przychody)*1.25)), xaxt = 'n',xlab="Tura", ylab="PLN", main = 'Wyniki symulacji bez optymalizacji')
axis(1, at=1:nrow(koszty),koszty$Tura)
abline(v = 15, lty = 2)

sredni_zysk = c(1:30)
sredni_zysk[c(1:16)] = mean(zysk$Zysk[c(1:16)]) 
sredni_zysk[c(16:30)] = mean(zysk$Zysk[c(16:16)]) 
sredni_zysk

lines(sredni_zysk,lty = 3,col="purple" )
lines(koszty$Koszt.w.turze, col="red")
points(przychody$Przychod, col="green")
lines(przychody$Przychod, col="green")
points(zysk$Zysk, col="blue")
lines(zysk$Zysk, col="blue")
dev.off()



png("tekst/pictures/algorytm_skala/trasy.png")
plot(trasy$Koszt, col="red", ylim=c(as.integer(min(trasy)-1.25),as.integer(max(trasy)*1.25)), xaxt = 'n',xlab="Tura", ylab="PLN", main = 'Œrednie wyniki tras')
axis(1, at=1:nrow(trasy),trasy$Tura)
lines(trasy$Koszt, col="red")
points(trasy$Przychod, col="green")
lines(trasy$Przychod, col="green")
points(trasy$Zysk, col="blue")
lines(trasy$Zysk, col="blue")

dev.off()
trasy <- read.csv("rezultaty/dwa/trasy.csv")
png("tekst/pictures/algorytm_skala/trasy2.png")
ggplot(data = trasy, aes(x = trasy$Tura, y=trasy$Zysk, color = trasy$Symbol)) + ggtitle("Zysk per trasa")+xlab("Zysk") + ylab("Tura")+ geom_line(aes(group=trasy$Symbol)) +geom_point() + theme_bw() + geom_hline(linetype="dashed",aes(yintercept=0))
dev.off()
