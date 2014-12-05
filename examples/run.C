Int_t run(Int_t nthreads=4,
         Int_t nbuff = 10,
         Bool_t graphics=kFALSE,
	 const char *geomfile="ExN03.root",
	 const char *xsec="xsec_FTFP_BERT_G496p02.root",
	 const char *fstate="fstate_FTFP_BERT_G496p02.root")
{
   gSystem->Load("libPhysics");
   gSystem->Load("libHist");
   gSystem->Load("libThread");
   gSystem->Load("libGeom");
   gSystem->Load("libVMC");
   gSystem->Load("../lib/libGeant_v");
   gSystem->Load("../lib/libXsec");
   CpuInfo_t  cpuInfo;
   MemInfo_t  memInfo;
   ProcInfo_t procInfo;  
   gSystem->GetCpuInfo(&cpuInfo, 10);
   gSystem->GetMemInfo(&memInfo);
   gSystem->GetProcInfo(&procInfo);
   cout << " BEGINNING " << endl;
   cout << " Mem Total = " << memInfo.fMemTotal << endl; 
   cout << " Mem Used = " << memInfo.fMemUsed << endl; 
   cout << " Mem Swapped = " << memInfo.fSwapUsed << endl; 
   cout << " Resident Memory = " << procInfo.fMemResident << endl; 
   cout << " Virtual Memory = " << procInfo.fMemVirtual << endl; 
   Int_t memRes0=procInfo.fMemResident; 
   Int_t memVirt0=procInfo.fMemVirtual; 
   Int_t ntotal   = 20;  // Number of events to be transported
   Int_t nbuffered  = nbuff;   // Number of buffered events
   TGeoManager::Import(geomfile);
   GeantPropagator *prop = GeantPropagator::Instance(ntotal, nbuffered);
   WorkloadManager *wmgr = WorkloadManager::Instance(nthreads);
   wmgr->SetNminThreshold(5*nthreads);
   prop->fNaverage = 500;   // Average number of tracks per event
   prop->fNperBasket = 128;   // Vector size
   prop->fEmin = 3.E-6; // [3 KeV] energy cut
// prop->fEmax = 0.03.; // [30MeV] used for now to select particle gun energy
   prop->fEmax = 0.03;
// Create the tab. phys process.
   prop->fProcess = new TTabPhysProcess("tab_phys", xsec, fstate);
   prop->fPrimaryGenerator = new GunGenerator(prop->fNaverage, 11, prop->fEmax, -8, 0, 0, 1, 0, 0);
   prop->fApplication = new MyApplication();
// gROOT->ProcessLine(".x factory.C+");   
// prop->fUseDebug = kTRUE;
// prop->fDebugTrk = 1;
   prop->fUseMonitoring = graphics;
   prop->PropagatorGeom(geomfile, nthreads, graphics);
   gSystem->GetProcInfo(&procInfo);
   gSystem->GetMemInfo(&memInfo);
   Int_t memRes1=procInfo.fMemResident; 
   Int_t memVirt1=procInfo.fMemVirtual;
   cout << " Typical memory for handling one correction:" << endl;
   cout << " Resident Memory = " << memRes1 -memRes0 << endl; 
   cout << " Virtual Memory = " << memVirt1-memVirt0 << endl; 
   cout << " Ending " << endl;
   cout << " *-------------------------------------* " << endl;
   cout << " Mem Total = " << memInfo.fMemTotal << endl; 
   cout << " Mem Used = " << memInfo.fMemUsed << endl; 
   cout << " Mem Swapped = " << memInfo.fSwapUsed << endl; 
   cout << " Resident Memory = " << procInfo.fMemResident << endl; 
   cout << " Virtual Memory = " << procInfo.fMemVirtual << endl; 
   cout << " *-------------------------------------* " << endl;
   return (memRes1 - memRes0);
}   
