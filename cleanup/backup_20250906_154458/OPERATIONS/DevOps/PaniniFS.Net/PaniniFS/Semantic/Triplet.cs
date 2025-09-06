using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PaniniFS.Semantic
{
    class Triplet
    {
        private static readonly log4net.ILog log =
    log4net.LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);


        // attention : la notion de fait en web sémantique ne semble pas gerer les sources d'affirmations
        // l'idée des hypernoeuds était de superposer les arbres de connaissances en commençant par les connaissances communes/publiques pour s'empiler vers le plus privé pour finir avec le transactionnel.

        // qu'en est-il des fonctions lexicales : particulièrement les réciproques. Peut on inférer?

        // Sujet
        // Verbe
        // objet

        // dbpedia

        // RDF SPARQL

        // RDF quads = triplet + graph tag

        // Très redondant comme formats, facile a alléger avec une hiérarchie. 
    }
}
