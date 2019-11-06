using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

/// <summary>
/// readtrack.cs - Reads a LEGO Stunt Rally track file. By Yellowberry, MIT license.
/// </summary>

namespace srtools
{
    class Readtrack
    {
        public static string lego_header;
        public static int crashint, trk_size, trk_theme, trk_time, trk_fsize, iters;
        public static long realsize;

        public static byte[][][][] trk_pieces;

        static void Main(string[] args)
        {
            string trk_name = "";
            try
            {
                trk_name = args[0];
            }
            catch (IndexOutOfRangeException)
            {
                Console.Beep();
                Console.WriteLine("Hey, you gotta provide an argument for the track!");
                System.Environment.Exit(1);
            }
            FileStream file = File.Open(trk_name, FileMode.Open, FileAccess.Read);
            using (BinaryReader reader = new BinaryReader(file))
            {
                realsize = file.Length;
                lego_header = bstr(reader.ReadBytes(12));
                crashint = bint(reader.ReadBytes(4));
                trk_fsize = bint(reader.ReadBytes(4));
                if (trk_fsize != 65576) throw new Exception("Binary filesize reports non 64KB file!");
                else if (trk_fsize != realsize) throw new Exception("Incorrect filesize, corrupted track!");
                trk_size = bint(reader.ReadBytes(4));
                trk_theme = bint(reader.ReadBytes(4));
                trk_time = bint(reader.ReadBytes(4));

                iters = 8 * (trk_size + 1);
                int skip = (56 - (trk_size * 8)) * 16;
                trk_pieces = new byte[iters][][][];

                for (int y = 0; y < iters; y++)
                {
                    byte[][][] tmp = new byte[iters][][];
                    for (int x = 0; x < iters; x++)
                    {
                        byte[][] piece = new byte[3][];
                        reader.ReadBytes(4);
                        for (int z = 0; z < 3; z++)
                        {
                            byte[] bytes = reader.ReadBytes(4);
                            piece[z] = bytes;
                        }
                        tmp[x] = piece;
                    }
                    reader.ReadBytes(skip);
                    trk_pieces[y] = tmp;
                }

                Console.WriteLine("## Track information for {0} ##", trk_name);
                Console.WriteLine("Fizesize: {0}", trk_fsize);
                Console.WriteLine("Track Type: {0}", LSRutil.t_size[trk_size]);
                Console.WriteLine("Track Theme: {0}", LSRutil.t_theme[trk_theme]);
                Console.WriteLine("Time of Day: {0}", LSRutil.t_time[trk_time]);
                Console.WriteLine("---");
                PrettyPiece(0,0);
            }
        }

        static string bstr(byte[] data)
        {
            string str;
            if (!BitConverter.IsLittleEndian) Array.Reverse(data);
            str = Encoding.UTF8.GetString(data);
            return str;
        }

        static int bint(byte[] data)
        {
            int i;
            if (!BitConverter.IsLittleEndian) Array.Reverse(data);
            i = BitConverter.ToInt32(data, 0);
            return i;
        }

        static int bchar(byte data)
        {
            int ch;
            ch = data;
            return ch;
        }

        static float bfloat(byte[] data)
        {
            float fl;
            if (!BitConverter.IsLittleEndian) Array.Reverse(data);
            fl = BitConverter.ToSingle(data, 0);
            return fl;
        }

        public static byte[] Combine(params byte[][] arrays)
        {
            byte[] ret = new byte[arrays.Sum(x => x.Length)];
            int offset = 0;
            foreach (byte[] data in arrays)
            {
                Buffer.BlockCopy(data, 0, ret, offset, data.Length);
                offset += data.Length;
            }
            return ret;
        }

        public static int GetTheme(byte theme)
        {
            int t = -1;

            if      (theme == 0x3B) t = 0; // Jungle
	        else if (theme == 0x3F) t = 1; // Ice
            else if (theme == 0x47) t = 2; // Desert
            else if (theme == 0x43) t = 3; // City
	        return t;
        }

        public static int GetNid(int id, int theme)
        {
            int ret = 0;

            int[] tb = { };

            if      (theme == 0) tb = LSRutil.pi_jung; // Jungle
	        else if (theme == 1) tb = LSRutil.pi_ice;  // Ice
	        else if (theme == 2) tb = LSRutil.pi_dsrt; // Desert
	        else if (theme == 3) tb = LSRutil.pi_city; // City

            foreach (int i in tb)
            {
                if (i == id) break;
                ret += 1;
            }

            return ret;
        }

        public static int[] ParsePiece(byte[][] data)
        {
            float height = bfloat(data[0]);
	        if      (height == -1) height = 0;
	        else if (height ==  8) height = 1;
	        else if (height == 16) height = 2;
	        else if (height == 24) height = 3;

            byte[] piece = data[1];
            int theme = GetTheme(piece[1]);
            int id = piece[0];
            int nid = GetNid(id, theme);
            int rotation = piece[2];

            return new int[5] { nid, id, theme, rotation, (int)height };
        }

        public static void PrettyPiece(int x, int y)
        {
            int[] info = ParsePiece(trk_pieces[y][x]);
            Console.WriteLine("### Piece information for x{0},y{1} ###", x, y);
            Console.WriteLine("nID: {0}", info[0]);
            Console.WriteLine("ID: {0:X}", info[1]);
            Console.WriteLine("Theme: {0}", LSRutil.t_theme[info[2]]);
            Console.WriteLine("Rotation: {0}", info[3]);
            Console.WriteLine("Height: {0}", info[4]);
        }
    }
}
