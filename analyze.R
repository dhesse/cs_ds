library(ggplot2)
library(dplyr)

data <- read.csv('game_log.csv')
data <- mutate(group_by(data, map), rounds=max(round) - min(round))

kpr <- summarise(group_by(data, killer, map), kpr=n()/nth(rounds,1))
mean_kpr <- summarise(group_by(kpr, killer), kpr=mean(kpr))

ggplot(mean_kpr, aes(x=reorder(killer, kpr), y=kpr)) +
    geom_bar(stat='identity') +
        coord_flip() +
            labs(x="Player", y="Kills per Round")

dpr <- summarise(group_by(data, victim, map), kpr=n()/nth(rounds,1))
mean_dpr <- summarise(group_by(dpr, victim), dpr=mean(kpr))

ggplot(mean_dpr, aes(x=reorder(victim, dpr), y=dpr)) +
    geom_bar(stat='identity') +
        coord_flip() +
            labs(x="Player", y="Deaths per Round")

popular_guns <- summarise(group_by(data, weapon), n=n())

ggplot(popular_guns, aes(x=reorder(weapon,n), y=n)) +
    geom_bar(stat='identity') +
        coord_flip() +
            labs(x="Gun", y="Number of kills")

qplot(killer, victim, data=data, geom="bin2d")
