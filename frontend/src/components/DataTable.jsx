import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableRow from '@mui/material/TableRow';
import TableHead from '@mui/material/TableHead';
import Typography from '@mui/material/Typography';


export default function DataTable({data}){
    if (!data) return null;

    // For list of objects
    if(Array.isArray(data)){
        if(data.length === 0){
        return <Typography variant="body2">No data available.</Typography>     
       }

       const headers = Object.keys(data[0]);

       return (
            <Table size='small'>
                <TableHead>
                    <TableRow>
                        {headers.map(header =>(
                            <TableCell key={header} sx={{fontWeight: 'bold'}}>
                                {header}
                            </TableCell>
                        ))}
                    </TableRow>
                </TableHead>
                <TableBody>
                    {data.map((row, i) =>(
                        <TableRow key={i}>
                            {headers.map(header => (
                                <TableCell key={header}>
                                    {row[header] !== null && typeof row[header] === 'object' 
                                    ? JSON.stringify(row[header])
                                    : row[header] ?? 'N/A'}

                                </TableCell>
                            ))}
                        </TableRow>
                    ))}
                </TableBody>
                
            </Table>
       );

    }

    // For single object
    if(typeof data === 'object'){
        return (
            <Table size='small'>
                <TableBody>
                    {Object.entries(data).map(([key, value]) => (
                        <TableRow key={key}>
                            <TableCell sx={{fontWeight: 'bold'}}> {key} </TableCell>
                            <TableCell>
                                {value !== null && typeof value === 'object'
                                 ? JSON.stringify(value) 
                                 : value ?? 'N/A' }
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>

            </Table>

        );
    }
 
 return null;

};