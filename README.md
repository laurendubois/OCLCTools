Started with OCLC and Alma exports in .mrc
Merge and reformat to tsv .txt
OCLC files look like - 
  001
  "ocm00000002\"
  "ocm00000017\"
  "ocm00000022\"
Alma files look like -
  001	035$a
  "991021576089705251"	"(TxHR)1908498-01rice_inst;(SIRSI)1908498;(OCoLC)968568862"
  "991021576099705251"	"(TxHR)3250329-01rice_inst;(SIRSI)3250329;(OCoLC)928889304"
  "991021576119705251"	"(TxHR)1976644-01rice_inst;(SIRSI)1976644;(OCoLC)58602699"
Run filecleanup.py on Alma files
Now Alma files look like -
  001	035$a
  "991021576089705251"	"968568862"
  "991021576099705251"	"928889304"
  "991021576119705251"	"58602699"
Run OCLC-simple-reclamation_LD_leadingzeros_alma.py
