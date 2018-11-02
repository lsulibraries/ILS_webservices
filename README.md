# ILS_webservices
Webservice API calls to Ebsco and Sirsi

# Sirsi
Sirsi Workflows, Sirsi eLibrary, and Sirsi Webservices return the same values.  Workflows has widest set of functionality.  Webservices has about 80% of Workflows' functions, and eLibrary has about 10%.  As of today, eLibrary is only used for the links on the [Enterprise search page](https://lsu.ent.sirsi.net/client/en_US/lsu) (Advanced Search, Browse Search, and Call Number Search links).


The Sirsi Enterprise search is a much better search than the above services, because it uses Apache solr.  There is currently no API for Enterprise. 


Using Sirsi Webservices for search is inferior to Enterprise, as it precludes using the solr functions in Enterprise.  Until an API for Enterprise becomes available, the only way to get Enterprise functionality is via the Enterprise view.


Non-search functions, however, are available through the Webservices Api, and could be very useful for managing users, looking up item details, setting items holds, etc.  The full list of Api functions is included in [this text file](https://github.com/lsulibraries/ILS_webservices/blob/master/SirsiWebservicesFunctions.txt).


# Ebsco API

Ebsco authentication works for both registered users and for IP range.  It also allows a toggle for showing some results to guest users versus blocking results to guest users.

You can send a search request via a REST call & get a json response.  You may specify limiters, expanders, facets, search fields, etc.  You may specify a full detail response, a brief response, or a very brief response.  It functions just like the webpage for Ebsco search, except that it uses REST and json format.  There is no view, naturally.

# Summary

The Ebsco service offers all the features inherent to Ebsco Discovery search (as far as I can tell).  The Sirsi service is limited to Symphony functions, and does not include the excellent solr-based Enterprise search engine.  While the Ebsco service is a good candidate for using webservices to build a custom view, the Sirsi service is not.

The degree of reliance on these services ranges from minimal to maximal.  You can use Ajax to add tiny webservice calls to an existing webapp.  Or you can build an entirely custom app from the ground up.  You are free to use them at whatever scope you choose.   
