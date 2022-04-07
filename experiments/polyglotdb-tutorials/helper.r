library(tidyverse)

mvt_outlier <- function (x, y, level_sd=4) {
  mat <- as.matrix(cbind(x,y))
  mu <- c(mean(mat[,1]), mean(mat[,2]))
  sigma <- cov(mat)
  out <- mahalanobis(mat, center=mu, cov=sigma) > level_sd
}

create_prototypes <- function (v, out=NULL, measurement_point=0.33) {
  v_proto <- v %>%
    mutate(A1A2diff = A1-A2,
           A2A3diff = A2-A3)
  
  # THE PARAMETERS FOR THE PROTOTYPES
  proto_parameters <- c('F1','F2','F3','B1','B2','B3','A1A2diff','A2A3diff')
  
  # REMOVE ROWS WITH NA FOR COLUMNS WE NEED FOR PROTOTYPES AND OMIT PHONES WITH FEWER THAN 6 REMAINING TOKENS
  v_proto <- v_proto[complete.cases(v_proto[,proto_parameters]),]
  lofreq_phones <- names(table(v_proto$phone))[table(v_proto$phone)<6]
  if (length(lofreq_phones)){
    v_proto <- filter(v_proto, !phone%in%lofreq_phones)
    print (paste('omitting low-frequency phone', lofreq_phones))
  }
  
  # CALCULATE THE MEANS AND COVARIANCE MATRICES
  corpus_means_for_phones <- v_proto[,c('phone', proto_parameters)] %>%
    mutate(type='means') %>%
    select(type, phone, proto_parameters) %>%
    group_by(type, phone) %>%
    summarise(across(proto_parameters, mean, na.rm=T)) %>%
    ungroup()
  
  names(corpus_means_for_phones)[names(corpus_means_for_phones)%in%proto_parameters] <- paste(names(corpus_means_for_phones)[names(corpus_means_for_phones)%in%proto_parameters], measurement_point, sep='_')
  
  corpus_covmats_list <- list()
  for (p in unique(v_proto$phone)) {
    corpus_covmats_list[[p]] <- v_proto %>%
      filter(phone==p) %>%
      dplyr::select(proto_parameters) %>%
      rename_with(function (x) {paste0(x, "_0.33")}) %>%
      cov() %>%
      data.frame(type="matrix", phone=p, .)
  }
  corpus_covmats <- bind_rows(corpus_covmats_list)
  
  phones_for_polyglot <- as.data.frame(
    bind_rows(
      corpus_means_for_phones,
      corpus_covmats
    )
  )
  
  if (!is.null(out)) {
    write.table(phones_for_polyglot, file=out, 
                row.names=F, sep=',', quote=FALSE)
  }
}


count_by_revised <- function (x) {
  cat("original: ", 
      nrow(filter(x, !revised)),
      "; revised: ",
      nrow(filter(x, revised)),
      "\n", sep=""
  )
  return(x)
}
