require 'csv'
require 'set'
require 'rexml/document'

include REXML

puts "Step 3: build mapping: EventType -> CVE -> AffectedOS/App ... "

# used files
file_event_to_cve = "file_1_1_event_to_cves.csv"
file_cve_to_os = "file_2_1_cve_to_os.csv"
file_cve_to_app = "file_2_2_cve_to_app.csv"
file_final_append = "../vulnerabilities.csv"


puts "load CVE to affected OS mapping ... "
cve_os_map = {}
CSV.open(file_cve_to_os, 'r') do |row|
	next if (row.length<2)
	cve = row[0]
	os_array = row[1].split(',')
	cve_os_map[cve] = os_array
	puts "#{cve} => #{os_array.join(",")}"
end

puts "load CVE to affected App mapping ... "
cve_app_map = {}
CSV.open(file_cve_to_app, 'r') do |row|
	next if (row.length<2)
	cve = row[0]
	app_array = row[1].split(',')
	cve_app_map[cve] = app_array
	puts "#{cve} => #{app_array.join(",")}"
end

os_app_name_map = {}
doc = Document.new(File.new("cpe/official-cpe-dictionary_v2.2.xml"))
XPath.each(doc, "cpe-list/cpe-item") do |cpe_item|
  cpe_name = cpe_item.attributes["name"].to_s.strip
  cpe_name = cpe_name[5..-1]
  title_node = cpe_item.get_elements("title[@xml:lang='en-US']")[0]
  cpe_title = title_node.get_text.value.strip
  os_app_name_map[cpe_name] = cpe_title
  puts "#{cpe_name} => #{cpe_title}"
end

# write result to ../vulnerabilities.csv
# format: #Bugtraq Id,CVE,Vendor Vulnerability,Vuln Description,Device Event Type,Affected OSVendor,Affected OSModel,Affected OSVersion,Affected AppVendor,Affected AppModel,Fixed Version,Fixed Patch,Fix ReleaseDate
file = File.open(file_final_append, "a")
file.write("\n")

puts "load event to CVE mapping ... "
CSV.open(file_event_to_cve, 'r') do |row|
	next if (row.length<2)
	event = row[0]
	cves = row[1].split(',')
	puts "#{event} => #{cves.join(",")}"

	# find OS
	os_array = cves.map { |cve| cve_os_map[cve]}
	os_array.flatten!	
	os_array.compact!
	os_array.uniq!
	next if (os_array==nil || os_array.empty?)
	os_array = os_array.map! { |os| os_app_name_map.has_key?(os) ? os_app_name_map[os] : os}
	
	# find App
	app_array = cves.map { |cve| cve_app_map[cve]}
	app_array.flatten!	
	app_array.compact!
	app_array.uniq!
	next if (app_array==nil || app_array.empty?)
	app_array = app_array.map! { |app| os_app_name_map.has_key?(app) ? os_app_name_map[app] : app }
	
	puts "#{event},\"#{cves.join(',')}\",\"#{os_array.join(',')}\",\"#{app_array.join(',')}\"\n"
	file.write(",\"#{cves.join(',')}\",,,#{event},,\"#{os_array.join(',')}\",,,\"#{app_array.join(',')}\",,,\n")
end
file.close

puts "generate all successfully @#{Time.new} ..."
