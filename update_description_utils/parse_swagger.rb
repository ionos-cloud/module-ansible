require "active_support/isolated_execution_state"
require 'oas_parser'

swagger_file = ARGV[0]
endpoint = ARGV[1]
verb = ARGV[2]

definition = OasParser::Definition.resolve(swagger_file)

parsed_endpoint = definition.path_by_path(endpoint).endpoint_by_method(verb)

if parsed_endpoint.request_body
    endpoint_info = parsed_endpoint.request_body.properties_for_format('application/json')[0].schema['properties']['properties']['properties']
else
    endpoint_info = parsed_endpoint.raw['parameters'].filter { |a| a['in'] == 'body' }.last['schema']['properties']['properties']['properties']
end

puts JSON[endpoint_info]
