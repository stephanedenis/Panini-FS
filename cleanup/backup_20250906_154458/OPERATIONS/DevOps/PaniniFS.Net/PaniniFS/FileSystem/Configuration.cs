using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PaniniFS.FileSystem
{
    class Configuration
    {

        private static readonly log4net.ILog log =
    log4net.LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        // Host workspace
        private string WorkingDir;
        public string VolumeLabel { get => VolumeLabel; private set => VolumeLabel = value; }

        // Grouping files by size allows clear view of decomposition to be addressed in priority
        Dictionary<string, long> BlobBucketStructure = new Dictionary<string, long>
        {
            ["2^10"] = 2 ^ 10,
            ["2^11"] = 2 ^ 11,
            ["2^12"] = 2 ^ 12,
            ["2^13"] = 2 ^ 13,
            ["2^14"] = 2 ^ 14,
            ["2^15"] = 2 ^ 15,
            ["2^16"] = 2 ^ 16,
            ["2^18"] = 2 ^ 18,
            ["2^20"] = 2 ^ 20,
            ["2^22"] = 2 ^ 22,
            ["2^24"] = 2 ^ 24,
            ["2^28"] = 2 ^ 28,
            ["2^32"] = 2 ^ 32,
        };


        public Configuration(string WorkingDir, string VolumeLabel="")
        {
            this.WorkingDir = WorkingDir;
            this.VolumeLabel = VolumeLabel;
        }



        /// <summary>
        /// Blobs ar stored in specific directories according to their size
        /// </summary>
        /// <param name="blobSize"></param>
        /// <returns>the complete path to the directory where the blob should be stored</returns>
        public string getBlobDir(long blobSize)
        {
            string size = "Oversize";
            foreach (string dirName in BlobBucketStructure.Keys)
            {
                if (blobSize < BlobBucketStructure[dirName])
                {
                    size = dirName;
                    break;
                }
            }
            return WorkingDir + @"\blobs\" + size;
        }


    }
}
