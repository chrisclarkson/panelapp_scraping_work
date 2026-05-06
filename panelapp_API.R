library(jsonlite)
rm(list=ls())
allPanels <- fromJSON("https://panelapp.genomicsengland.co.uk/WebServices/list_panels/")
panelGenes <- NULL

for(p in allPanels$result$Name){
  panelweb <- gsub(" ","%20",p)
  myjson <-fromJSON(paste0("https://panelapp.genomicsengland.co.uk/WebServices/get_panel/",panelweb,"/"))
  genes <- as.data.frame(cbind(myjson$result$Genes$GeneSymbol,
                               myjson$result$Genes$LevelOfConfidence,
                               myjson$result$Genes$Penetrance,
                               myjson$result$Genes$ModeOfInheritance),
                         stringsAsFactors = F)
  if (ncol(genes) == 4){
    colnames(genes) <- c("GeneSymbol","LevelOfConfidence","Penetrance","ModeOfInheritance")
    genes$PanelName <- p
    genes$MutationType='gene'
    panelGenes <- rbind(panelGenes, genes)
  }
  strs <- as.data.frame(cbind(myjson$result$STRs$GeneSymbol,
                               myjson$result$Genes$LevelOfConfidence,
                               myjson$result$Genes$Penetrance,
                               myjson$result$Genes$ModeOfInheritance), 
                         stringsAsFactors = F)
  if (ncol(strs) == 4){
    colnames(strs) <- c("GeneSymbol","LevelOfConfidence","Penetrance","ModeOfInheritance")
    strs$PanelName <- p
    strs$MutationType='STRs'
    panelGenes <- rbind(panelGenes,genes,strs)
  }
}

panel <- data.frame(allPanels$result$Name,
                    allPanels$result$CurrentVersion,
                    allPanels$result$DiseaseSubGroup,
                    allPanels$result$DiseaseGroup,
                    unlist(lapply(allPanels$result$Relevant_disorders,function(x){paste(x,collapse = '/')})),
                    unlist(lapply(allPanels$result$PanelTypes,function(x){paste(x,collapse = '/')})),
      stringsAsFactors = F)
colnames(panel) <- c("PanelName","CurrentVersion","DiseaseSubGroup","DiseaseGroup","RelevantDisorders","PanelTypes")
# panelGenes2=panelGenes
# panelGenes=panelGenes2
# panelGenes$PanelTypes=unlist(lapply(panelGenes$PanelTypes,function(x){paste(x,collapse = '/')}))
panelGenes$CurrentVersion=unlist(panelGenes$CurrentVersion)
panelGenes$DiseaseSubGroup=unlist(panelGenes$DiseaseSubGroup)
panelGenes$DiseaseGroup=unlist(panelGenes$DiseaseGroup)
panelGenes3 <- merge(panelGenes, panel, by="PanelName")
# panelGenes=panelGenes3[panelGenes3$LevelOfConfidence=='HighEvidence',]
# panelGenes=panelGenes[grep(pattern = 'gms',panelGenes$PanelTypes),]
write.table(panelGenes3,'panel_genes_types_included.tsv',sep='\t',row.names = F,quote = F)

