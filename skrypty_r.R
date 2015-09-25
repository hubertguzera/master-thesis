setwd("C:/Users/Hubert/Desktop/master-thesis/master-thesis/")

#tabela cech produkty
library(xtable)
produkty <- read.csv("rezultaty/produkt.csv")
print(xtable(produkty))

#profile klientow
decyzje <- read.csv("rezultaty/decyzje.csv")
decyzje_s <- decyzje[decyzje$Wybor=="Symulowane",]
png("tekst/pictures/profile_klientow.png")
par(mfrow = c(2,2))
plot(density(decyzje$Wiek), ylab = "Gęstość", main = "Rozkład zmiennej wiek", ylim = c(0,0.025), lty = 2)
lines(density(decyzje_s$Wiek), col="blue")

plot(density(decyzje$Zarobki), ylab = "Gęstość", main = "Rozkład zmiennej zarobki", ylim = c(0,0.0015), lty = 2)
lines(density(decyzje_s$Zarobki), col="blue")

library(sm)
sm.density.compare(decyzje_s$Zarobki,decyzje$Zarobki)

plot(density(decyzje$Kobieta), ylab = "Gęstość", main = "Rozkład zmiennej płeć", ylim = c(0,4), lty = 2)
lines(density(decyzje_s$Kobieta), col="blue")

a <- cbind(tabulate(decyzje$Wyksztalcenie)/nrow(decyzje),tabulate(decyzje_s$Wyksztalcenie)/nrow(decyzje_s))
barplot(a, beside=TRUE, col=c("gray70", "gray60","gray50","gray40", "deepskyblue1","deepskyblue2","deepskyblue3","deepskyblue4"), ylab = "Procent",main = "Histogram zmiennej wykształcenie", ylim = c(0,0.5), lty = 2)
axis(1, at=(1:10), c("Brak","Podstawowe","Zawodowe","Średnie","Wyższe","Brak","Podstawowe","Zawodowe","Średnie","Wyższe"))
lines(rep(sum(decyzje_s$Wyksztalcenie==1)/nrow(decyzje_s),10),lty=2, col="deepskyblue1")
lines(rep(sum(decyzje_s$Wyksztalcenie==2)/nrow(decyzje_s),10),lty=2, col="deepskyblue2")
lines(rep(sum(decyzje_s$Wyksztalcenie==3)/nrow(decyzje_s),10),lty=2, col="deepskyblue3") 
lines(rep(sum(decyzje_s$Wyksztalcenie==4)/nrow(decyzje_s),10),lty=2, col="deepskyblue4") 
dev.off()

a <- as.data.frame(table(decyzje$Tura,decyzje$Wybor))
library(ggplot2)
png("tekst/pictures/sprzedaz_marek.png")
par(mfrow = c(1,1))
ggplot(data = a, aes(x = a$Var1, y=a$Freq, color = a$Var2)) + ggtitle("Wyniki sprzedaży poszczególnych marek")+xlab("Tura") + ylab("Sprzedaż")+ geom_line(aes(group=a$Var2)) +geom_point() + theme_bw() + scale_colour_discrete(name = "Marki") + theme(legend.position="bottom")
dev.off()

png("tekst/pictures/ilosc_klientow.png")
par(mfrow = c(1,1))
plot(as.data.frame(table(decyzje$Tura))[,2], ylim=c(1500,2500), ylab="Ilość klientów", xlab="Tura", main="Ilość klientów we wszystkich sklepach")
lines(as.data.frame(table(decyzje$Tura))[,2])
lines(lty=2, col="gray", rep(mean(as.data.frame(table(decyzje$Tura))[,2]),length(as.data.frame(table(decyzje$Tura))[,2])))
axis(1, at=(1:30), c(1:30))
dev.off()


#prognozy
prognozaLM <- read.csv("rezultaty/LM/prognoza.csv")
prognozaKM <- read.csv("rezultaty/KM/prognoza.csv")
prognozaLM <- aggregate(prognozaLM[3:4], by=list(prognozaLM$Tura), FUN="sum")
prognozaKM <- aggregate(prognozaKM[3:4], by=list(prognozaKM$Tura), FUN="sum")

par(mfrow = c(1,1))

#skuteczność przewidywań
przewidywania <- read.csv("rezultaty/KM/przewidywania.csv")
sum(przewidywania$K.Mean==1)
przewidywania <- read.csv("rezultaty/LM/przewidywania.csv")
sum(przewidywania$LM==1)


#wyniki firmy

koszty <- read.csv("rezultaty/lm/koszty.csv")
koszty <- aggregate(koszty[5], by=list(koszty$Tura), FUN="sum")
przychody <- read.csv("rezultaty/lm/przychody.csv")
przychody <- aggregate(przychody[5], by=list(przychody$Tura), FUN="sum")
zysk <- read.csv("rezultaty/lm/zysk.csv")
trasy <- read.csv("rezultaty/lm/trasy.csv")


par(mfrow = c(1,1))
png("tekst/pictures/przychody_koszty_lm.png")
plot(koszty$Koszt.w.turze,pch=19, col="red", ylim=c(750,as.integer(max(koszty,przychody)*1.25)), xaxt = 'n',xlab="Tura", ylab="PLN", main = 'Przychody (zielony) i koszty (czerwnony) przedsiębiorstwa')
axis(1, at=1:nrow(koszty),koszty$Tura)
abline(v = 20, lty = 2)
lines(koszty$Koszt.w.turze, col="red")
points(przychody$Przychod, col="green", pch=19)
lines(przychody$Przychod, col="green")
dev.off()


png("tekst/pictures/zysk_lm.png")
plot(zysk$Zysk, pch=19, col="purple", ylim=c(-400,500), xaxt = 'n',xlab="Tura", ylab="PLN", main = 'Zysk przedsiębiorstwa')
lines(zysk$Zysk,col="purple")
sredni_zysk = c(1:30)
sredni_zysk[c(1:20)] = mean(zysk$Zysk[c(1:20)]) 
sredni_zysk[c(21:30)] = mean(zysk$Zysk[c(21:30)]) 
lines(x=c(1:20), y=sredni_zysk[c(1:20)],lty = 3,col="red" )
lines(x=c(21:30), y=sredni_zysk[c(21:30)],lty = 3,col="green" )
abline(v = 20, lty = 2)
dev.off()

koszty <- read.csv("rezultaty/km/koszty.csv")
koszty <- aggregate(koszty[5], by=list(koszty$Tura), FUN="sum")
przychody <- read.csv("rezultaty/km/przychody.csv")
przychody <- aggregate(przychody[5], by=list(przychody$Tura), FUN="sum")
zysk <- read.csv("rezultaty/km/zysk.csv")
trasy <- read.csv("rezultaty/km/trasy.csv")

par(mfrow = c(1,1))
png("tekst/pictures/przcyhody_koszty_kn.png")
plot(koszty$Koszt.w.turze,pch=19, col="red", ylim=c(750,as.integer(max(koszty,przychody)*1.25)), xaxt = 'n',xlab="Tura", ylab="PLN", main = 'Przychody (zielony) i koszty (czerwnony) przedsiębiorstwa')
axis(1, at=1:nrow(koszty),koszty$Tura)
abline(v = 20, lty = 2)
lines(koszty$Koszt.w.turze, col="red")
points(przychody$Przychod, col="green", pch=19)
lines(przychody$Przychod, col="green")
dev.off()



png("tekst/pictures/zysk_km.png")
plot(zysk$Zysk, pch=19, col="purple", ylim=c(-1000,500), xaxt = 'n',xlab="Tura", ylab="PLN", main = 'Zysk przedsiębiorstwa')
lines(zysk$Zysk,col="purple")
sredni_zysk = c(1:30)
sredni_zysk[c(1:20)] = mean(zysk$Zysk[c(1:20)]) 
sredni_zysk[c(21:30)] = mean(zysk$Zysk[c(21:30)]) 
lines(x=c(1:20), y=sredni_zysk[c(1:20)],lty = 3,col="red" )
lines(x=c(21:30), y=sredni_zysk[c(21:30)],lty = 3,col="green" )
abline(v = 20, lty = 2)
dev.off()

png("tekst/pictures/trasy.png")
ggplot(data = trasy, aes(x = trasy$Tura, y=trasy$Oblozenie, color = trasy$Symbol))+scale_colour_discrete(guide = FALSE) + ggtitle("Wolumen alokowany przez algorytm na każdą ze ścieżek")+xlab("Tura") + ylab("Wolumen")+ geom_line(aes(group=trasy$Symbol)) +geom_point() + theme_bw() + geom_hline(linetype="dashed",aes(yintercept=0)) + scale_colour_discrete(name = "Scieżki") + theme(legend.position="bottom")
dev.off()

prognozy_2 <- read.csv("rezultaty/skutecznosc_przewidywan.csv",header=FALSE)
colnames(prognozy_2) <- c("Symbol","Tura","Prawdziwe","KN","LG")
prognozy_2$Tura <- prognozy_2$Tura +1
prognozy_2 <- aggregate(prognozy_2[c(3,4,5)], by=list(prognozy_2$Tura), FUN="sum")

png("tekst/pictures/rozklad_prognoz.png")
skutecznosc <- read.csv("rezultaty/przewidywania2.csv",s=";")
plot(density(skutecznosc$Lm), col="blue",xlim=c(0,1), ylab="Gęstość",main="Rozkład prawdopodobieństwa zakupu według metod prognozowania")
lines(density(skutecznosc$KM),col="red")
dev.off()

