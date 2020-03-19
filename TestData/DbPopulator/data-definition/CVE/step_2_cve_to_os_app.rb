require 'csv'
require 'set'
require 'rexml/document'
require 'phoenix_util'

include REXML

puts "Step 2: parse XML to Hash<CVE, Array<AffectedOS/AffectedApp>> ... "

# check two files generated in step 1
file_event_to_cves = "file_1_1_event_to_cves.csv"
file_cve_set = "file_1_2_cve_set.csv"
puts "file_1_1_event_to_cves.csv not exist!" unless File.exist?(file_event_to_cves)
puts "file_1_2_cve_set.csv not exist!" unless File.exist?(file_cve_set)

# to generate four files in step 2
file_cve_to_os = "file_2_1_cve_to_os.csv"
file_cve_to_app = "file_2_2_cve_to_app.csv"
file_os_set = "file_2_3_os_set.csv"
file_app_set = "file_2_4_app_set.csv"
File.delete(file_cve_to_os) if File.exist?(file_cve_to_os)
File.delete(file_cve_to_app) if File.exist?(file_cve_to_app)
File.delete(file_os_set) if File.exist?(file_os_set)
File.delete(file_app_set) if File.exist?(file_app_set)


# @param file: 		cpe data 2.0 XMLs, such as "./nvdcve-2.0/nvdcve-2.0-recent.xml"
# @param cve_set:	ignored CVEs
# @param cve_to_os:	output - reutrn Hash<CVE, Array<AffectedOS>>
# @param cve_to_app:output - reutrn Hash<CVE, Array<AffectedApp>>
# @param os_set:	output - TODO-rui, 
# @param app_set:	output - TODO-rui
NS = {"cpe-lang" => "http://cpe.mitre.org/language/2.0", "vuln" => "http://scap.nist.gov/schema/vulnerability/0.4"}
def xml2cve_os_app_map(file, cve_set, cve_os_map, cve_app_map, os_set, app_set)
	doc = Document.new(File.new(file))
	XPath.each(doc, "nvd/entry") do |nodeCVE|
		cve = nodeCVE.attributes["id"].to_s.strip
		next if (!cve_set.member?(cve))
		os_array = []
		app_array = []
		XPath.each(nodeCVE, "vuln:vulnerable-software-list/vuln:product", NS) do |nodeSW|
			sw_name = nodeSW.text
			# puts sw_name
			if (sw_name.index("cpe:/o:") == 0)
				os_array << sw_name[5..-1]
			elsif (sw_name.index("cpe:/a:") == 0)
				app_array << sw_name[5..-1]			
			end
		end
		next if (os_array.empty? && app_array.empty?)
		
		# for affected OS
		puts os_array
		os_array.compact!
		os_array.uniq!
		os_array.map { |e| e.strip! }
		os_set.merge(os_array)
		puts os_array
		cve_os_map[cve] = os_array if (!os_array.empty?)
		
		# for affected App
		puts app_array
		app_array.compact!
		app_array.uniq!
		app_array.map { |e| e.strip! }
		app_set.merge(app_array)
		puts app_array
		cve_app_map[cve] = app_array if (!app_array.empty?)
	end
end


# read used CVE from file generated in step 1
cve_set = Set.new()
CSV.open(file_cve_set, 'r') do |row|
	next if (row.length<1 || row[0]==nil)
	cve_set.add(row[0])
end

# collect all XMLs by order
# file_list = Dir["./nvdcve-2.0/nvdcve-2.0-2003.xml"]
file_list = Dir["./nvdcve-2.0/nvdcve-2.0-2*.xml"]
file_list << "./nvdcve-2.0/nvdcve-2.0-recent.xml"
file_list << "./nvdcve-2.0/nvdcve-2.0-modified.xml"

# parse CVE XMLs to cve_os_map and cve_app_map
cve_os_map = {}
cve_app_map = {}
os_set = Set.new()
app_set = Set.new()
file_list.each do |file|
	xml2cve_os_app_map(file, cve_set, cve_os_map, cve_app_map, os_set, app_set)
	puts "parsed XML #{file} successfully @#{Time.new} ..."
end


# write result to files
print_map_to_file(cve_os_map, file_cve_to_os)
print_map_to_file(cve_app_map, file_cve_to_app)
print_set_to_file(os_set, file_os_set)
print_set_to_file(app_set, file_app_set)

puts "Step 2 Done ... "
