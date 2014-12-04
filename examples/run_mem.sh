#!/bin/bash
threads=$1
nbuff=$2
/Users/oksanashadura/CERN/ROOT/bin/root -b -q /Users/oksanashadura/CERN_sources/GeantV/vecprot_v2/run.C\($threads\,$nbuff\,false,\"/Users/oksanashadura/CERN_sources/GeantV/vecprot_v2/ExN03.root\",\"/Users/oksanashadura/CERN_sources/GeantV/vecprot_v2/xsec_FTFP_BERT_G496p02.root\",\"/Users/oksanashadura/CERN_sources/GeantV/vecprot_v2/fstate_FTFP_BERT_G496p02.root\"\)
