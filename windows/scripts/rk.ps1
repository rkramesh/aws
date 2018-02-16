function Import-Certificate{
     param([String]$certPath,[String]$certRootStore,[String]$certStore)
     $pfx=new-object System.Security.Cryptography.X509Certificates.X509Certificate2
     $pfx.import($certPath)
     $store= new-object System.Security.Cryptography.X509Certificates.X509Store($certStore,$certRootStore)
     $store.open("MaxAllowed")
     $store.add($pfx)
     $store.close()
}

#Import-Certificate "$(Split-Path $MyInvocation.MyCommand.Path)\test.cer" "Currentuser" "TrustedPublisher"
Import-Certificate "C:\Users\rk\test-folder\test.cer" "Currentuser" "TrustedPublisher"
