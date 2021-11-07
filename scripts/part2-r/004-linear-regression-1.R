## ----cache=FALSE, echo=FALSE--------------------------------------------------
## use num signif digits (which is what
## tidy print does by default) instead of decimal 
options(knitr.digits.signif = TRUE)
options(digits = 3)


## ----ch4-libraries, cache=FALSE, message=F, error=F, warning=F, echo=1:3------
library(languageR)
library(tidyverse)
library(broom)
library(sjPlot)
select <- dplyr::select # to prevent masking by MASS::select

library(feather)


## ----ch4_datasets-------------------------------------------------------------
neutralization <- read.csv('data/neutralization_rmld.csv', stringsAsFactors = TRUE)


## ----ch4-functions, cache=FALSE, echo=FALSE-----------------------------------
# 
# slrCoeffReport <- function(mod, coeff_name, sig_fig=3){
#   tab <- mod %>% tidy(conf.int=TRUE) %>% filter(term==coeff_name)
#   paste("$\\hat{\\beta} =",
#         signif(tab$estimate, sig_fig),
#         "$, $t(", mod$df.residual,
#         ")=", signif(tab$statistic, sig_fig),
#         '$, ',
#         formatP(tab$p.value), ", 95\\% CI $[",
#         signif(tab$conf.low, sig_fig),
#         ", ",
#         signif(tab$conf.high, sig_fig),
#         "]$",
#         sep='')
# }

## override default printing method of tibbles: now they are just 
## printed like dataframes
#
# print.tbl_df <- function(x, ...) {
#   print.data.frame(x, row.names=FALSE, ...)
#   invisible(x)
# }


## -----------------------------------------------------------------------------
english <- mutate(english, AgeSubject =  relevel(AgeSubject, 'young'))


## ----slr-ex-1, echo=FALSE, fig.height=3, fig.width=3, out.width='45%', warning=FALSE, fig.cap="Scatterplot of \\ttt{RTlexdec} as a function of \\ttt{WrittenFrequency} (left) and \\ttt{AgeSubject} (right), for the \\ttt{english} dataset. Lines show least-squares lines of best fit, which for the right plot is the line between group means."----
filter(english, AgeSubject=='young') %>%
ggplot(aes(WrittenFrequency, RTlexdec)) +
  geom_point(size=0.25) + stat_smooth(method='lm') +
  xlab("Word frequency") + ylab("Reaction time") +
  ggtitle("Young subjects only")

english %>% ggplot(aes(AgeSubject, RTlexdec)) +
  geom_jitter(width=0.1, height=0, size=0.25) +
  stat_summary(fun.y="mean", geom="line", color="blue", size=1, group=1) +
  xlab("Subject age") + ylab("Reaction time") +
  ggtitle("All subjects")


## ----output.lines=4:11--------------------------------------------------------
cor.test(~WrittenFrequency + RTlexdec, data=english)

## ----echo=FALSE---------------------------------------------------------------
ct <- cor.test(~WrittenFrequency + RTlexdec, data=english)


## -----------------------------------------------------------------------------
select(english, WrittenFrequency, RTlexdec) %>% head(n=5)

## ----echo=FALSE---------------------------------------------------------------
my_mat <- select(english, WrittenFrequency, RTlexdec) %>% head(n=5)


## -----------------------------------------------------------------------------
english_young <- filter(english, AgeSubject == "young")
slr_mod_1 <- lm(RTlexdec ~ WrittenFrequency, data = english_young)


## -----------------------------------------------------------------------------
coefficients(slr_mod_1)


## -----------------------------------------------------------------------------
summary(slr_mod_1)


## -----------------------------------------------------------------------------
confint(slr_mod_1)


## ----dependson=c('ch4-libraries')---------------------------------------------
tidy(slr_mod_1, conf.int = TRUE)


## ----young-subset-1, fig.height=3, fig.width=3, out.width='50%', fig.cap="Reaction time versus word frequency (as in Fig.~\\ref{fig:slr-ex-1} left), for a subset of 25 points from young speakers in the \\ttt{english} dataset. Line and shading are  least-squares line of best fit and 95\\% CI."----
set.seed(2903)
young_sample <- english_young %>% sample_n(25)

ggplot(young_sample, aes(WrittenFrequency, RTlexdec)) +
  geom_point() +
  geom_smooth(method="lm")


## ----eval=FALSE---------------------------------------------------------------
## slr_mod_2 <- lm(RTlexdec~WrittenFrequency, data=young_sample)


## ----echo=FALSE---------------------------------------------------------------
slr_mod_2 <- lm(RTlexdec~WrittenFrequency, data=young_sample)
coeff_string <- slrCoeffReport(slr_mod_2, 'WrittenFrequency', 2)


## ----dependson=c('ch4-libraries')---------------------------------------------
tidy(slr_mod_2, conf.int = TRUE) %>%
  select(term, statistic, p.value, conf.low, conf.high)


## -----------------------------------------------------------------------------
summary(slr_mod_2)$r.squared


## ----eval=FALSE---------------------------------------------------------------
## slr_mod_3 <- lm(RTlexdec ~ AgeSubject, data=english)


## ----echo=FALSE---------------------------------------------------------------
slr_mod_3 <- lm(RTlexdec ~ AgeSubject, data=english)
slr_mod_3_report <- slrCoeffReport(slr_mod_3, 'AgeSubjectold', 3)


## ----output.lines=4:8---------------------------------------------------------
t.test(RTlexdec ~ AgeSubject, data = english, var.equal=TRUE)


## ----output.lines=4:11--------------------------------------------------------
cor.test(young_sample$WrittenFrequency, young_sample$RTlexdec)


## ----mlr_mod_1_def------------------------------------------------------------
mlr_mod_1 <- lm(RTlexdec~WrittenFrequency+AgeSubject, data = english)


## ----output.lines=8:18--------------------------------------------------------
summary(mlr_mod_1)

## -----------------------------------------------------------------------------
confint(mlr_mod_1)


## ----mlr_tab, echo=FALSE, dependson=c('ch4-libraries', 'mlr_mod_1_def')-------
mlr_tab_1 <- tidy(mlr_mod_1) %>% mutate(estimate = signif(estimate,2))
test <- mlr_tab_1[1,'estimate']


## -----------------------------------------------------------------------------
predict(mlr_mod_1, english[3,]) 


## -----------------------------------------------------------------------------
## four new observations:
new_df <- expand.grid(AgeSubject=c('young','old'), WrittenFrequency=c(5,6))

## add model predictions for each observation:
new_df$prediction <- predict(mlr_mod_1, new_df)

new_df


## ----eval=FALSE---------------------------------------------------------------
## mlr_mod_2 <- lm(vowel_dur ~ voicing, data = neutralization)
## summary(mlr_mod_2)


## ----echo=FALSE---------------------------------------------------------------
mlr_mod_2 <- lm(vowel_dur ~ voicing, data = neutralization)
## repeated from last chapter so this one compiles alone


## -----------------------------------------------------------------------------
glance(mlr_mod_2) %>% print(width=Inf)


## ----ixn-ex-1, fig.align='center', fig.height=3, fig.width=4, out.width='45%', fig.cap="Empirical summaries of effects of two predictors on a response.  Left (\\ttt{english} data): line of best fit with 95\\% CIs for word frequency effect on reaction time, for each subject age group. Right (\\ttt{neutralization} data): mean and 95\\% bootstrapped CI for each combination of consonant voicing and prosodic boundary presence.", echo=FALSE----
ggplot(english, aes(WrittenFrequency, RTlexdec)) +
  geom_point(size=0.2) +
  geom_smooth(method="lm", aes(color=AgeSubject))


filter(neutralization, !is.na(prosodic_boundary)) %>% 
  ggplot(aes(x=voicing, y=vowel_dur)) + 
  stat_summary(fun.data='mean_cl_boot', aes(color=prosodic_boundary)) +
  stat_summary(fun.data='mean_cl_boot', geom='line', aes(group=prosodic_boundary, color=prosodic_boundary))


## ----mlr_mod_3_chunk, echo=1:2------------------------------------------------
mlr_mod_3 <- lm(vowel_dur ~ prosodic_boundary + voicing +
                  voicing:prosodic_boundary, data=neutralization)

# write out since needed in later chapters TODO: hide
saveRDS(mlr_mod_3, file=paste('objects/', 'mlr_mod_3.rds', sep='')
)


## ----eval=FALSE---------------------------------------------------------------
## lm(vowel_dur ~ voicing*prosodic_boundary, data=neutralization)


## ----echo=FALSE---------------------------------------------------------------
mlr_mod_3_tab <- mlr_mod_3 %>% tidy(conf.int=TRUE)


## ----dependson=c('mlr_mod_3_chunk'), size='small', echo=1---------------------
 mlr_mod_3 %>% tidy(conf.int=TRUE) %>% select(term, estimate, p.value)
mlr_tab_3 <-  mlr_mod_3 %>% tidy(conf.int=TRUE)


## ----eval=FALSE---------------------------------------------------------------
## plot_model(mlr_mod_3, type='pred', terms = c('voicing'))
## plot_model(mlr_mod_3, type='pred', terms = c('prosodic_boundary'))


## ----eval=FALSE---------------------------------------------------------------
## plot_model(mlr_mod_3, type='pred',
##            terms = c('voicing', 'prosodic_boundary'),
##            title="Voicing x prosodic boundary")


## ----mlr-mod-3-plots, echo=FALSE, fig.width=4, fig.height=3, out.width='45%', fig.cap="Two plots for interpretation of the \\ttt{voicing}:\\ttt{prosodic\\_boundary} interaction.  Left: model predictions with 95\\% CIs for model \\ttt{mlr\\_mod\\_3}. Right: empirical means and 95\\% CIs."----
plot_model(mlr_mod_3, type='pred', terms = c('voicing', 'prosodic_boundary'), title="Model predictions")

filter(neutralization, !is.na(prosodic_boundary)) %>% 
  ggplot(aes(x=voicing, y=vowel_dur)) + 
  stat_summary(fun.data='mean_cl_boot', aes(color=prosodic_boundary)) +
  ggtitle("Empirical data")


## ----eval=FALSE---------------------------------------------------------------
## filter(neutralization, !is.na(prosodic_boundary)) %>%
##   ggplot(aes(x=voicing, y=vowel_dur)) +
##   stat_summary(fun.data='mean_cl_boot', aes(color=prosodic_boundary)) +
##   ggtitle("Empirical data")


## -----------------------------------------------------------------------------
## exclude very infrequent accent_type (n=11) for this example
neut_sub <- filter(neutralization, accent_type!='deaccented')

## relevel factor so that 
# accented (nuclear) > unaccented (prenuclear)
neut_sub <- mutate(neut_sub, accent_type = relevel(accent_type, 'prenuclear'))
mlr_bad_mod_1 <- lm(vowel_dur ~ prosodic_boundary*voicing + accent_type, 
                data=neut_sub)


## -----------------------------------------------------------------------------
 mlr_bad_mod_1 %>% tidy(conf.int=TRUE) %>% select(term, estimate, p.value)


## ----mlr-bad-mod-plots, echo=FALSE, fig.width=4, fig.height=3, out.width='45%', fig.cap="Two plots for interpretation of the \\ttt{voicing}:\\ttt{prosodic\\_boundary} interaction in model \\ttt{mlr\\_bad\\_mod\\_1}. Left: model predictions with 95\\% CIs.  Right: empirical means and 95\\% CIs.  "----
plot_model(mlr_bad_mod_1, type='pred', terms = c('voicing', 'prosodic_boundary'), title="Model predictions")

filter(neut_sub, !is.na(prosodic_boundary)) %>% 
  ggplot(aes(x=voicing, y=vowel_dur)) + 
  stat_summary(fun.data='mean_cl_boot', aes(color=prosodic_boundary)) +
  ggtitle("Empirical data")


## -----------------------------------------------------------------------------
neutralization <- neutralization %>% 
  mutate(voicing =  relevel(voicing, 'voiceless'))

# . ~ . means "same model formula"
# model is refit using new 'neutralization' dataframe
mlr_mod_4 <- update(mlr_mod_3, . ~ ., data=neutralization)


## -----------------------------------------------------------------------------
mlr_mod_4 %>% tidy() %>% select(term, estimate)


## ----echo=FALSE---------------------------------------------------------------
mlr_mod_3_summ <- mlr_mod_3 %>% glance()


## ----echo = FALSE, warning=FALSE, message=FALSE, results = 'asis'-------------
tidy(mlr_mod_3) %>% 
  select(one_of('estimate', 'std.error', 'statistic', 'p.value'))  %>% 
add_column(coeff=c('Intercept', 'Prosodic boundary', 'Voicing', 'PB:Voicing'), .before=1) %>% 
  printWrapper(pCol='p.value')

