# Genera la figura del mapa de clientes para la presentación (mismo PCA de los Módulos 15-17)
library(ggplot2)
credit <- read.csv("../data/bronze/synthetic_credit_card_customer_behavior_dataset.csv")
num <- names(credit)[sapply(credit, is.numeric)]
excluir <- c("Monthly_Spending", "Payment_Ratio", "Credit_Utilization", "Reward_Points_Earned", "Outstanding_Balance")
ret <- setdiff(num, excluir)
sk <- function(x) mean(((x - mean(x)) / sd(x))^3)
X <- credit[, ret]; lv <- ret[abs(sapply(X, sk)) > 1]; X[lv] <- lapply(X[lv], log1p)
p <- prcomp(scale(X))
C1 <- sign(sum(p$rotation[, 1])) * p$x[, 1]
C2 <- -sign(p$rotation["Credit_Score", 2]) * p$x[, 2]
lista <- rank(credit$Credit_Score, ties.method = "first") <= 8195
zona <- ifelse(!lista, "Sin seguimiento", ifelse(C1 > median(C1), "A", "B"))
stopifnot(sum(zona == "A") == 3939, sum(zona == "B") == 4256)
set.seed(17); i <- sample(nrow(credit), 9000)
d <- data.frame(C1 = C1[i], C2 = C2[i], zona = factor(zona[i], c("Sin seguimiento", "B", "A")))
d <- d[order(d$zona), ]
g <- ggplot(d, aes(C1, C2, color = zona)) +
  geom_point(size = 1.1, alpha = 0.55, stroke = 0) +
  geom_vline(xintercept = median(C1), linetype = 2, color = "#14213D", linewidth = 0.5) +
  scale_color_manual(values = c("Sin seguimiento" = "#C9CED6", B = "#F4A259", A = "#D7263D"), guide = "none") +
  labs(x = "TAMAÑO DEL CLIENTE (C1)  →", y = "RIESGO (C2)  →") +
  theme_minimal(base_size = 15) +
  theme(panel.grid = element_blank(), axis.text = element_blank(),
        axis.title = element_text(color = "#5B6475", face = "bold", size = 13),
        plot.background = element_rect(fill = "white", color = NA))
ggsave("presentacion/mapa_clientes.png", g, width = 9, height = 6.6, dpi = 220)

# Mapa por tipo de tarjeta: se ordena en tamaño, se monta en riesgo
niv <- c("Basic", "Silver", "Gold", "Platinum", "Signature")
dt <- data.frame(C1 = C1[i], C2 = C2[i], tarjeta = factor(credit$Card_Type[i], niv))
g2 <- ggplot(dt, aes(C1, C2, color = tarjeta)) +
  geom_point(size = 1, alpha = 0.45, stroke = 0) +
  stat_ellipse(level = 0.9, linewidth = 1.3) +
  scale_color_manual(values = c(Basic = "#9AA5B8", Silver = "#5DA9E9", Gold = "#E9B44C",
                                Platinum = "#2E4057", Signature = "#7B2CBF"), name = NULL) +
  guides(color = guide_legend(override.aes = list(size = 4, alpha = 1, linewidth = 0))) +
  labs(x = "TAMAÑO DEL CLIENTE (C1)  →", y = "RIESGO (C2)  →") +
  theme_minimal(base_size = 15) +
  theme(panel.grid = element_blank(), axis.text = element_blank(), legend.position = "top",
        legend.text = element_text(size = 14, color = "#14213D"),
        axis.title = element_text(color = "#5B6475", face = "bold", size = 13),
        plot.background = element_rect(fill = "white", color = NA))
ggsave("presentacion/mapa_tarjetas.png", g2, width = 9, height = 6.6, dpi = 220)
