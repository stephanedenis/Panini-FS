using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PaniniFS.Storage
{
    class BinCodec
    {
        // finalement base64 est plus simple et stable à cause des noms de fichiers
        // 512 bits = 64 bytes = 80 charactères en base 64



        // inspiré par yEncode... mauvaise idée pour les SHA512, mais ok pour intégrer un long blob dans un fichier texte
        // ~ pour signifier le début d'un bloc empreinte SHA de 512 bits encodé par escape code ~
        // ~i = ~
        // ~n = null
        // ~r = return
        // ~l = line feed
        // ~s = space
        // ~t = tab
        // ~d = .
        // ~c = :
        // ~
        //      en texte libre, Le bloc encodé peut donc être étalé sur plusieurs lignes

        // https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file


    }
}
