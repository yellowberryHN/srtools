using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace srtools
{
    class Gentrack
    {
        public static string lego_header = "LEGO MOTO\x00\x00";
        public static int trk_cst_version = 1;

        public static int trk_size = 1; // 0 - Multi, 1 - Single
        public static int trk_theme = 3; // 0 - Jungle, 1 - Ice, 2 - Desert, 3 - City
        public static int trk_time = 1; // 0 - Day, 1 - Night
        public static string trk_comment = "Hey, this is a test of a track comment. Pretty nifty.";

        static void Main(string[] args)
        {

            string trk_name = "";
            try
            {
                trk_name = args[0];
            }
            catch (IndexOutOfRangeException)
            {
                trk_name = "csharp.trk";
            }
            using (BinaryWriter writer = new BinaryWriter(File.Open(trk_name, FileMode.Create)))
            {
                Random rnd = new Random();
                // Write magic number, and custom track info
                writer.Write(Encoding.ASCII.GetBytes(lego_header));
                writer.Write((byte)trk_cst_version);

                // The Crash byte, has to be 5
                writer.Write(bc(5));

                writer.Write(bc(65576)); // Filesize (65576), game will only recognize files with this specific file size
                writer.Write(bc(trk_size)); // Track Size
                writer.Write(bc(trk_theme)); // Track Scenery Theme
                writer.Write(bc(trk_time)); // Track Time of Day

                int loop = 8 * (trk_size + 1);
                AddPiece(writer, 0, 0); // make the start line
                for (int y = 0; y < loop - 1; y++)
                {
                    AddPiece(writer, 30, rnd.Next(4), rnd.Next(4), rnd.Next(4)); // build track
                }
                AddTrackPad(writer, trk_size);

                for (int y = 0; y < loop - 1; y++)
                {
                    for (int x = 0; x < loop; x++)
                    {
                        AddPiece(writer, 30, rnd.Next(4), rnd.Next(4), rnd.Next(4)); // build track
                    }
                    AddTrackPad(writer, trk_size);
                }

                // This outputs 85 80 03 for some reason before the null bytes, fix eventually
                writer.Write("".PadRight(65572 - (int)writer.BaseStream.Position - 3, '\0'));

                writer.Write(bc(1));
                Console.WriteLine("Wrote {0} bytes.", writer.BaseStream.Position);
            }
        }

        static byte[] bc(float data)
        {
            byte[] bytes = BitConverter.GetBytes(data);
            if (!BitConverter.IsLittleEndian) Array.Reverse(bytes);
            return bytes;
        }

        static byte[] bc(int data)
        {
            byte[] bytes = BitConverter.GetBytes(data);
            if (!BitConverter.IsLittleEndian) Array.Reverse(bytes);
            return bytes;
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

        static byte[] CalcHeight(int height) // 0 - 3
        {
            float h = 0;
            if (height == 0) h = -1; // -1 (BF 80 00 00)
            else
            {
                if      (height == 1) h = 8;  //  8 (41 00 00 00)
                else if (height == 2) h = 16; // 16 (41 80 00 00)
                else if (height == 3) h = 24; // 24 (41 C0 00 00)
            }
            return bc(h); // Little endian float (DCBA)
        }

        static int CalcTheme(int theme = -1) // 0 - 3
        {
            int t = 0;
            if (theme == -1) return CalcTheme(trk_theme); // cheap trick to pass the track theme instead
            else
            {
                if      (theme == 0) t = 0x3B; // Jungle
                else if (theme == 1) t = 0x3F; // Ice
                else if (theme == 2) t = 0x47; // Desert
                else if (theme == 3) t = 0x43; // City
            }
            return t;
        }

        static byte[] CalcPiece(int id, int theme)
        {
            byte p = 0;
            if (id == -1) return new byte[4] { 0, 0, 0, 0 }; // Empty piece
            else
            {
                if (theme == -1) theme = trk_theme;

                if      (theme == 0) p = (byte)LSRutil.pi_jung[id]; // Jungle
                else if (theme == 1) p = (byte)LSRutil.pi_ice[id];  // Ice
                else if (theme == 2) p = (byte)LSRutil.pi_dsrt[id]; // Desert
                else if (theme == 3) p = (byte)LSRutil.pi_city[id]; // City
            }
            return new byte[] { p, (byte)CalcTheme(theme), 0, 0 };
        }

        static void AddPiece(BinaryWriter writer, int pieceId = -1, int rotation = 0, int height = 0, int pieceTheme = -1)
        {
            byte[][] track =
            {
            bc(0), // Null bytes, Unknown
	        CalcHeight(height), // Height, managed by calcHeight()
	        CalcPiece(pieceId, pieceTheme), // Piece ID and Theme
            bc(rotation) // Rotation
            };

            writer.Write(Combine(track));
        }

        static void AddTrackPad(BinaryWriter writer, int size)
        {
            int amt = 56 - size * 8; // 48 for single, 56 for multi

            for (int runs = 0; runs < amt; runs++)
            {
                writer.Write(new byte[] { 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 255, 255, 0, 0, 0, 0 });
            }
        }
    }
}
