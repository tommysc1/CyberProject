using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Threading;
using System.IO.Pipes;
using System.IO;

namespace CyberProjectGUI
{
    public partial class Form1 : Form
    {
        public delegate void dele();
        /// <summary>
        /// Contains column names.
        /// </summary>
        List<string> _names = new List<string>();

        /// <summary>
        /// Contains column data arrays.
        /// </summary>
        List<string[]> _dataArray = new List<string[]>();

        public Form1()
        {
            InitializeComponent();

            
            // Render the DataGridView.
            dataGridView1.DataSource = GetResultsTable();
            Thread engine = new Thread(new ThreadStart(PipeReader));
            engine.Start();

            NamedPipeServerStream server = new NamedPipeServerStream("Orders");
            server.WaitForConnection();
            
        }

        public DataTable GetResultsTable()
        {
            // Create the output table.
            DataTable d = new DataTable();

            // Loop through all process names.
            for (int i = 0; i < this._dataArray.Count; i++)
            {
                // The current process name.
                string name = this._names[i];

                // Add the program name to our columns.
                d.Columns.Add(name);

                // Add all of the memory numbers to an object list.
                List<object> objectData = new List<object>();

                // Put every column's numbers in this List.
                foreach (string data in this._dataArray[i])
                {
                    objectData.Add((object)data);
                }

                // Keep adding rows until we have enough.
                while (d.Rows.Count < objectData.Count)
                {
                    d.Rows.Add();
                }

                // Add each item to the cells in the column.
                for (int a = 0; a < objectData.Count; a++)
                {
                    d.Rows[a][i] = objectData[a];
                }
            }
            return d;
        }




        public void PipeReader()
        {
            // Open the named pipe.
            var server = new NamedPipeServerStream("Data");

            //Console.WriteLine("Waiting for connection...");
            server.WaitForConnection();

            //Console.WriteLine("Connected.");
            var br = new BinaryReader(server);
            //var bw = new BinaryWriter(server);

            while (true)
            {
                try
                {
                    var len = (int)br.ReadUInt32();            // Read string length
                    if (len == 0)
                        continue;
                    var str = new string(br.ReadChars(len));    // Read string
                    string[] clients = str.Split(';');
                    this._names = new List<string>();
                    this._dataArray = new List<string[]>();
                    for (int i = 0; i < clients.Length; i++) 
                    {
                        string name = clients[i].Split('%')[0];
                        this._names.Add(name);
                        string[] dates = (clients[i].Split('%')[1]).Split(',');
                        this._dataArray.Add(dates);
                    
                    }

                    dele invokeDELE = new dele(this.updateDataGrid);
                    this.Invoke(invokeDELE);

                   


                    //Console.WriteLine("Read: " + str);
                }
                catch (EndOfStreamException)
                {
                    break;                    // When client disconnects
                }
            }

            MessageBox.Show("Engine has disconnected");
            server.Close();
            server.Dispose();

        }

        public void updateDataGrid() 
        {
            dataGridView1.DataSource = typeof(DataTable);
            dataGridView1.DataSource = GetResultsTable();
        }











    }
}
