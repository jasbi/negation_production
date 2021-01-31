
|FUNCTION|Linguistic Composition|Examples|
|------|--------|--------------------|--------------------|
|Rejection| With *like* or *want* | "I not like it", "not want it" |
|Epistemic | know, think, remember  | "I not know" |
|Prohibition | with imperative subjectless *do* | "do not spill milk"|
|Inability | with modal *can* | "I cannot zip it"|
|Labeling | modifying nominal or adjectival predicatives | "that's not a crocodile"; "it's no interesting"|
|Non-existence | expletives; with a nominal; *no more* | "there is no soup"; "no juice"; "no more milk" | 
|Possession | have; with possesive pronouns| "not have the toy"; "not mine" | 
  
  
|Domain|Functions|Linguistic Composition|Examples|
|------|--------|--------------------|--------------------|
|Emotion|Rejection| With *like* or *want* | "I not like it", "not want it" |
|Theory of Mind| Epistemic | know, think, remember  | I not know |
|Motor Control| Prohibition, Inability | with imperative subjectless *do* or modal *can* | "do not spill milk", "I cannot zip it"|
|Language Learning| Labeling | modifying nominal or adjectival predicatives | "that's not a crocodile"; "it's no interesting"|
|Perception| non-existence; possession | expletives; with a nominal, more-N; have | no juice, no more milk, not in there, the dog not barking | 
  
|Unknown | Temporal | now, today, again | not today |
|Unknown | Causal | why | why not? |
|Unknown | Posession | 's or pronouns, or have | not mine |
  
|Domain|Functions|Linguistic Composition|Examples|
|------|--------|--------------------|--------------------|
|Emotion|Rejection| With *like* or *want* | "I not like it", "not want it" |
|Motor Control| Prohibition, Inability | with imperative subjectless *do* or modal *can* | "do not spill milk", "I cannot zip it"|
|Perception| non-existence | with a nominal, more-N, or locatives, event descriptions | no juice, no more milk, not in there, the dog not barking | 
|Language Learning| Labeling | modifying predicative nominals | that's not a crocodile |
|Theory of Mind| Epistemic | know, think, remember  | I not know |
|Unknown | Temporal | now, today, again | not today |
|Unknown | Causal | why | why not? |
|Unknown | Posession | 's or pronouns, or have | not mine |

### Causal

To search for expressions that articulate causal inquiry (*why not try*), we focused on instances that contain the phrase *why not*. In order to separate from other domains, again here we excluded cases where the head verb of the utterance overlaps with the head verbs in the domains analyzed above. This led to a total of X utterances.

```{r causaldata, include=FALSE}

causal <-read.csv('data/neg_causal.txt', header = T, sep = '\t')
causal$Role[which(causal$Role == "Father")] <- 'Parent'
causal$Role[which(causal$Role == "Mother")] <- 'Parent'
causal$Role[which(causal$Role == "Target_Child")] <- 'Child'

child_causal <- subset(causal, Role %in% c('Child'))
child_causal_know <- subset(child_causal, Head == 'know')
child_causal_remember <- subset(child_causal, Head == 'remember')
child_causal_think <- subset(child_causal, Head == 'think')
 
parent_causal <- subset(causal, Role %in% c('Parent'))
parent_causal_know <- subset(parent_causal, Head == 'know')
parent_causal_remember <- subset(parent_causal, Head == 'remember')
parent_causal_think <- subset(parent_causal, Head == 'think')

child_causal_know <- data.frame(table(child_causal_know$Age))
child_causal_know$Role <- rep('Child', nrow(child_causal_know))
child_causal_know$Head <- rep('know', nrow(child_causal_know))
child_causal_know$Ratio <- child_causal_know$Freq / sum(child_causal_know$Freq)

child_causal_remember <- data.frame(table(child_causal_remember$Age))
child_causal_remember$Role <- rep('Child', nrow(child_causal_remember))
child_causal_remember$Head <- rep('remember', nrow(child_causal_remember))
child_causal_remember$Ratio <- child_causal_remember$Freq / sum(child_causal_remember$Freq)

child_causal_think <- data.frame(table(child_causal_think$Age))
child_causal_think$Role <- rep('Child', nrow(child_causal_think))
child_causal_think$Head <- rep('think', nrow(child_causal_think))
child_causal_think$Ratio <- child_causal_think$Freq / sum(child_causal_think$Freq)

parent_causal_know <- data.frame(table(parent_causal_know$Age))
parent_causal_know$Role <- rep('Parent', nrow(parent_causal_know))
parent_causal_know$Head <- rep('know', nrow(parent_causal_know))
parent_causal_know$Ratio <- parent_causal_know$Freq / sum(parent_causal_know$Freq)

parent_causal_remember <- data.frame(table(parent_causal_remember$Age))
parent_causal_remember$Role <- rep('Parent', nrow(parent_causal_remember))
parent_causal_remember$Head <- rep('remember', nrow(parent_causal_remember))
parent_causal_remember$Ratio <- parent_causal_remember$Freq / sum(parent_causal_remember$Freq)

parent_causal_think <- data.frame(table(parent_causal_think$Age))
parent_causal_think$Role <- rep('Parent', nrow(parent_causal_think))
parent_causal_think$Head <- rep('think', nrow(parent_causal_think))
parent_causal_think$Ratio <- parent_causal_think$Freq / sum(parent_causal_think$Freq)

causal_data <- rbind(child_causal_think, child_causal_remember, child_causal_know, parent_causal_think, parent_causal_remember, parent_causal_know)
names(causal_data) <- c('Age', 'Freq', 'Role', 'Head', 'Ratio')

```

```{r causal, fig.env="figure", fig.pos = "H", fig.align = "center", fig.width=3.5, fig.height=5.5, set.cap.width=T, num.cols.cap=1, fig.cap = "Causal" }

causal_data %>% 
  ggplot(aes(as.numeric(Age), round(Ratio, 2), group = Role, color = Role)) +
  geom_point(aes(color = Role, shape = Role)) +
  scale_shape_manual(values = c(16, 3)) +
  scale_color_manual(values = c("steelblue", "peru")) + 
  geom_line(aes(color = Role, linetype = Role)) + 
  facet_grid(vars(Head)) +
  scale_x_continuous(breaks=seq(0, 72, 6)) +
  theme_classic() + 
  theme(text = element_text(size=10, family="Times")) + 
  theme(legend.position="top") +
  xlab("child age (months)") + 
  ylab("ratio")

```

### Event description


### Possession 
