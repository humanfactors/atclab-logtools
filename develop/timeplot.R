library(animation)
library(scatterplot3d)

df <- read.csv("coords.csv", header = FALSE)

# Interruption length 27s ~=~ 1 - 60/(length(df$x)/27)
ani.options(interval = 0.01405)

saveVideo({
    for (i in 1:nrow(df)) {
    pt <- df[i,]
    plot(x = pt[[1]], y = pt[[2]], xlim = c(0,65), ylim = c(0,52))}
}, movie.name = "animation.mp4")