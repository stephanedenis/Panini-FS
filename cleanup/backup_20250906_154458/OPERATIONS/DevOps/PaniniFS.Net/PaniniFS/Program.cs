using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using DokanNet;
using Panini.FileSystem;
using PaniniFS.FileSystem;

namespace PaniniFS
{
    class Program
    {
        private static readonly log4net.ILog log =
    log4net.LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        public static Configuration configuration;

        static void Main(string[] args)
        {
            // TODO parse args to set working dir and drive letter
            configuration = new Configuration(@"C:\PaniniFS");

            try
            {
                var pfs = new DokanOperations();
                pfs.Mount(@"P:\", DokanOptions.DebugMode | DokanOptions.StderrOutput);
                Console.WriteLine(@"Success");
            }
            catch (DokanException ex)
            {
                Console.WriteLine(@"Error: " + ex.Message);
            }
        }
    }
}
