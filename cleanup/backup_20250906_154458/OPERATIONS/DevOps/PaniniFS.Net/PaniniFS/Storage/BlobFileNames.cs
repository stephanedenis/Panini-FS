using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PaniniFS.Storage
{
    class BlobFileNames
    {
        Blob blob;
        VirtualFile[] files;

        public BlobFileNames(Blob blob)
        {
            this.blob = blob;
        }
    }
}
