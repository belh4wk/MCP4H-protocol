using System;
using System.IO;
using System.Text;
using System.Timers;
using System.Collections.Generic;
using Newtonsoft.Json.Linq;
// using SimHub.Plugins;           // Uncomment after adding SimHub references

namespace Mcp4hSimHubPlugin
{
    // TODO: inherit the correct SimHub base and interfaces for your SDK version, e.g.:
    // public class Plugin : IPlugin, IDataPlugin, IWPFSettingsV2
    public class Plugin /* : IPlugin, IDataPlugin */
    {
        private FileSystemWatcher _watcher;
        private string _varsPath;
        private Dictionary<string, object> _cache = new Dictionary<string, object>(StringComparer.OrdinalIgnoreCase);

        public string PluginName => "MCP4H Traction LEDs";

        // TODO: Wire these to SimHub property registration methods in your SDK version.
        private void SetProperty(string name, object value)
        {
            _cache[name] = value;
            // Example (SDK-dependent):
            // this.AddProperty("MCP4H", name, value);
        }

        public void Init(/*PluginManager pluginManager*/)
        {
            // Locate JSON file produced by Python bridge (adjust path if needed)
            _varsPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Plugins", "Mcp4h", "SimHubVars.json");
            Directory.CreateDirectory(Path.GetDirectoryName(_varsPath));

            _watcher = new FileSystemWatcher(Path.GetDirectoryName(_varsPath))
            {
                Filter = Path.GetFileName(_varsPath),
                NotifyFilter = NotifyFilters.LastWrite | NotifyFilters.Size
            };
            _watcher.Changed += (s, e) => Reload();
            _watcher.EnableRaisingEvents = true;

            Reload();
        }

        private void Reload()
        {
            try
            {
                if (!File.Exists(_varsPath)) return;
                string json;
                using (var fs = new FileStream(_varsPath, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                using (var sr = new StreamReader(fs, Encoding.UTF8))
                    json = sr.ReadToEnd();
                var jo = JObject.Parse(json);

                foreach (var kv in jo)
                {
                    var name = kv.Key;
                    var val = kv.Value.Type == JTokenType.Boolean ? (object)kv.Value.Value<bool>()
                              : kv.Value.Type == JTokenType.Integer ? (object)kv.Value.Value<int>()
                              : kv.Value.Type == JTokenType.Float ? (object)kv.Value.Value<double>()
                              : kv.Value.Type == JTokenType.String ? (object)kv.Value.Value<string>()
                              : kv.Value.ToString();

                    SetProperty(name, val);
                }
            }
            catch (Exception ex)
            {
                // TODO: log via SimHub logger if available
                Console.WriteLine("MCP4H plugin reload error: " + ex.Message);
            }
        }

        public void End()
        {
            _watcher?.Dispose();
        }
    }
}
