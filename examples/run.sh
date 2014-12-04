#!/bin/bash
threads=$1
vector=$2
/Users/oksanashadura/CERN/ROOT/bin/root -b -q /Users/oksanashadura/CERN_sources/GeantV/vecprot_v2/run.C\($threads\,$vector\,false,\"/Users/oksanashadura/CERN_sources/GeantV/vecprot_v2/ExN03.root\",\"/Users/oksanashadura/CERN_sources/GeantV/vecprot_v2/xsec_FTFP_BERT.root\",\"/Users/oksanashadura/CERN_sources/GeantV/vecprot_v2/fstate_FTFP_BERT.root\"\)
