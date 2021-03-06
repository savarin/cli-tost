# tost-cli

*This project was completed as a part of Bradfield's API class.*

## Introduction

tost is a text snippets API with a capability-based permissions model.

## Components

* [tost](https://github.com/savarin/tost) - server API
* [tost-client](https://github.com/savarin/tost-client) - client library
* [tost-cli](https://github.com/savarin/tost-cli) - command line interface
* [tost-web](https://github.com/savarin/tost-web) - web interface


## Example

    $ tost signup alice@example.com
    > successful signup for alice@example.com with id 37ecd127
    
    $ tost login 37ecd127
    > successful login for alice@example.com with id 37ecd127
    
    $ tost create foo
    > successful create for tost with access token b1d6cefb
    
    $ tost view b1d6cefb
    > b1d6cefb: foo
    
    
    $ tost signup bob@example.com
    > successful signup for bob@example.com with id 66ddfcc8
    
    $ tost login 66ddfcc8
    > successful login for bob@example.com with id 66ddfcc8
    
    $ tost view b1d6cefb
    > 5f3bd80c: foo
    # bob is granted access to alice’s tost simply by accessing the grant alice uses to access the document
    # bob gets his own grant
    
    
    $ tost signup carol@example.com
    > successful signup for carol@example.com with id 12c52e0e
    
    $ tost login 12c52e0e
    > successful login for carol@example.com with id 12c52e0e
    
    $ tost view 5f3bd80c
    > 10a5245e: foo
    # carol is granted access to alice’s tost simply by accessing the grant bob uses to access the document
    # carol gets her own grant
    
    
    $ tost login 37ecd127
    > successful login for alice@example.com with id 37ecd127
    
    $ tost access b1d6cefb
    > 5f3bd80c: bob@example.com
    > 10a5245e: carol@example.com
    > successful access request
    # alice reviews grants to access the document
    
    $ tost disable b1d6cefb 5f3bd80c
    > successful disable for tost with access token 5f3bd80c
    # alice revokes bob’s access, which in turn revokes carol’s access
