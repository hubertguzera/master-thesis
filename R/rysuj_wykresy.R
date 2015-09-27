setwd("C:/Users/Hubert/Desktop/master-thesis/master-thesis/")
getwd()

wykonanie <- read.csv("funkcje/stirling.csv",header=FALSE)
plot(wykonanie$V1,wykonanie$V3)
lines(wykonanie$V4, col="red")

#Ludnosc
ludnosc <- read.csv("rezultaty/lm/ludnosc.csv")
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

plot(x=ludnosc$wyksztalcenie,y=ludnosc$zarobki, ylab="Zarobki", xlab="Wykszta³cenie", main = 'Rozk³ad zmiennej zarobki w zale¿noœci od wykszta³cenia')
ludnosc$wyksztalcenie <- as.factor(ludnosc$wyksztalcenie)


produkty <- read.csv("rezultaty/produkty.csv")
print(xtable(produkty))
dev.off()

#Prognozy

prognoza <- read.csv("rezultaty/prognoza.csv")
prognoza <- aggregate(prognoza[3:4], by=list(prognoza$Tura), FUN="sum")
png("tekst/pictures/prog.png")
plot(prognoza$Przewidywane, col="blue", ylim=c(0,as.integer(max(prognoza)*1.25)), xaxt = 'n',xlab="Tura", ylab="Iloœæ produktów", main = 'Prognoza sprzeda¿y i rzeczywista sprzeda¿ produktów')
axis(1, at=1:nrow(prognoza),prognoza$Group.1)
lines(prognoza$Przewidywane, col="blue")
points(prognoza$Sprzedaz, col="green")
lines(prognoza$Sprzedaz, col="green")
dev.off()


#Wyniki firmy z optymalizacji 2
koszty <- read.csv("rezultaty/koszty.csv")
koszty <- aggregate(koszty[5], by=list(koszty$Tura), FUN="sum")
przychody <- read.csv("rezultaty/przychody.csv")
przychody <- aggregate(przychody[5], by=list(przychody$Tura), FUN="sum")
zysk <- read.csv("rezultaty/zysk.csv")
trasy <- read.csv("rezultaty/trasy.csv")




png("tekst/pictures/algorytm_skala/wyniki.png")
plot(koszty$Koszt.w.turze, col="red", ylim=c(as.integer(-max(koszty)*1.25),as.integer(max(przychody)*1.25)), xaxt = 'n',xlab="Tura", ylab="PLN", main = 'Wyniki symulacji bez optymalizacji')
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


library(ggplot2)
dev.off()
trasy <- read.csv("rezultaty/trasy.csv")
png("tekst/pictures/algorytm_skala/trasy2.png")
ggplot(data = trasy, aes(x = trasy$Tura, y=trasy$Oblozenie, color = trasy$Symbol))+scale_colour_discrete(guide = FALSE) + ggtitle("Zysk per trasa")+xlab("Zysk") + ylab("Tura")+ geom_line(aes(group=trasy$Symbol)) +geom_point() + theme_bw() + geom_hline(linetype="dashed",aes(yintercept=0))
dev.off()
library(sm)
decyzje <- read.csv("rezultaty/decyzje.csv")
decyzje_s <- decyzje[decyzje$Wybor=="Symulowane",]
plot(density(decyzje$Wiek))
lines(density(decyzje_s$Wiek), col="blue")
