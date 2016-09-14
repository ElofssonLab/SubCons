#!/usr/bin/env Rscript
library(ggplot2)
library(reshape)

args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
} else if (length(args)==1) {
  # default output file
  args[2] = "out.txt"
}

split_path <- function(path) {
rev(setdiff(strsplit(path,"/|\\\\")[[1]], ""))
}

files<- list.files(path=args[1],pattern="*.csv", full.names=T, recursive=FALSE)

myfun <- function(filex) {
data<-read.table(filex,sep="\t",header=T)
data<-data[2:10]
data.1<-melt(data)
data.1<-data.1[with(data.1,order (rev((variable)))),]
p <- ggplot(data=data.1,aes(x=Tools,y=value,fill=variable))+geom_bar(width=.4,stat="identity",colour="black")+coord_flip()+ scale_fill_manual(values = c("#33499a", "#ed3747","#008000", "#f9971a", "#a04c97","#12CFF5","#66CC00","#FF007F"))
p <- p + theme_bw()+theme(axis.line = element_line(colour = "black"),axis.title.y=element_blank(),panel.grid.major =element_blank(), panel.grid.minor = element_blank(),panel.border = element_blank(),panel.grid = element_blank(),panel.background = element_rect(colour = "black"))
p <- p + theme(legend.title = element_blank(),legend.key = element_blank())+ylab('Score')
p <- p + theme(axis.title = element_text(size = 15))
p<-p+scale_y_continuous(expand = c(0,0))+ scale_x_discrete(expand = c(0,0))
name<-strsplit(split_path(filex)[1],".csv")[[1]]
p <- p + guides(fill = guide_legend(reverse = TRUE)) + ggtitle(paste("Prediction result for:",name,sep=" "))
p <- p + guides(fill = guide_legend(reverse = TRUE))
ggsave(filename=paste(args[1],"/",paste(name,".pdf",sep=''),sep=""), plot=p,dpi = 500)
}

invisible(lapply(files, myfun))

