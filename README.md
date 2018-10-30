# ILS_webservices
Webservice API calls to Ebsco and Sirsi

# Sirsi
Sirsi Workflows, Sirsi eLibrary, and Sirsi Webservices return the same values.  Workflows has widest set of functionality.  Webservices has about 80% of Workflows' functions, and eLibrary has about 10%.  As of today, eLibrary is only used for the links on the [Enterprise search page](https://lsu.ent.sirsi.net/client/en_US/lsu) (Advanced Search, Browse Search, and Call Number Search links).


The Sirsi Enterprise search is a much better search than the above services, because it uses Apache solr.  There is currently no webservices for Enterprise. 


Using Sirsi webservices for search is inferior to Enterprise, as it precludes using the solr functions in Enterprise.  Until an API for Enterprise becomes available, the only way to get Enterprise functionality is via the Enterprise view.


Non-search functions are available through the Webservices Api, and could be useful for managing users, looking up item details, setting items holds, etc.  The full list of Api functions is included in [this text file](https://github.com/lsulibraries/ILS_webservices/blob/master/SirsiWebservicesFunctions.txt).