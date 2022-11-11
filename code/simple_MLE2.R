library(stringr)
library(data.table)
dat <- fread('/Users/user/Documents/NGramPolarization/trigrams2.csv')
dat[, ngram := str_sub(V1,2,-2)]; dat[, count := as.integer(V2)]; dat[, label := V3]; dat[, V1:=NULL]; dat[, V2:=NULL]; dat[, V3:=NULL]
dat[, total_count := sum(count), by = .(ngram, label)]; dat[, count := NULL]
dat<-unique(dat)
dat_inf <- dat[label == 'INFORMATIVE']
dat_inf[, label := NULL]; dat_inf[, inf_count := total_count]; dat_inf[, total_count := NULL]
dat_mis <- dat[label == 'MISINFORMATION']
dat_mis[, label := NULL]; dat_mis[, mis_count := total_count]; dat_mis[, total_count := NULL]
dat_cb <- merge( dat_inf, dat_mis, by = 'ngram', all = T)
dat_cb[is.na(inf_count), inf_count := 0]; dat_cb[is.na(mis_count), mis_count := 0]
dat_cb[, total_app := mis_count+inf_count]; dat_cb[, mis_freq := mis_count/total_app]
dat_cb_x <- dat_cb[total_app > quantile(dat_cb$total_app, .99)]
dat_cb_x[order(-mis_freq)]
fwrite(dat_cb_x[order(-mis_freq)], 'final_trigrams_ordered.csv')

